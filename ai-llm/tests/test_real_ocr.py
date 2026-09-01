import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OCR_PROJECT = PROJECT_ROOT / "ocr-cv"
IMAGE_PATH = PROJECT_ROOT / "test_images" / "product.jpeg"


def run_ocr():
    """Run Member 2 OCR in its own Python process."""

    code = f"""
from app.ocr.paddle_ocr import OCRProcessor
import json

processor = OCRProcessor()
result = processor.extract(r"{IMAGE_PATH}")

print(json.dumps(result, ensure_ascii=False))
"""

    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=OCR_PROJECT,
        capture_output=True,
        text=True,
        check=True,
    )

    # Paddle/PaddleX may print logs to stdout.
    # Find the JSON object containing the OCR result.
    output = result.stdout

    json_start = output.find("{")

    if json_start == -1:
        raise RuntimeError(
            f"Could not find OCR JSON output.\n{output}"
        )

    return json.loads(output[json_start:])


def main():
    print("Running Member 2 OCR...")

    ocr_result = run_ocr()

    print(
        f"OCR regions detected: "
        f"{len(ocr_result['regions'])}"
    )

    print("\nOCR TEXT:")
    print(ocr_result["text"])

    print("\nRunning Member 3 AI extraction...")

    # Import YOUR app only after the OCR subprocess has finished.
    from app.llm_service import extract_product

    product = extract_product(ocr_result)

    print("\nPRODUCT DATA:")
    print(product.model_dump_json(indent=2))

    # --------------------------------------------------
    # 1. Verify the complete ProductData contract
    # --------------------------------------------------

    expected_fields = {
        "manufacturer_packer_importer",
        "common_or_generic_name",
        "is_imported",
        "country_of_origin",
        "net_quantity",
        "consumer_care_details",
        "unit_sale_price",
        "selling_price",
        "mrp",
        "mrp_inclusive_of_taxes",
        "manufacturing_date",
        "packing_date",
        "import_date",
        "best_before",
        "use_by",
        "package_type",
    }

    actual_fields = set(product.model_dump().keys())

    assert actual_fields == expected_fields, (
        f"ProductData fields do not match.\n"
        f"Missing: {expected_fields - actual_fields}\n"
        f"Unexpected: {actual_fields - expected_fields}"
    )

    # --------------------------------------------------
    # 2. Verify important extracted fields
    # --------------------------------------------------

    assert product.manufacturer_packer_importer is not None
    assert product.common_or_generic_name is not None
    assert product.net_quantity is not None
    assert product.mrp is not None
    assert product.manufacturing_date is not None
    assert product.use_by is not None

    # --------------------------------------------------
    # 3. Verify fields that should remain unknown
    # --------------------------------------------------

    # The OCR does not explicitly establish that the
    # product is imported.
    assert product.is_imported is None

    # No import date is visible in the OCR.
    assert product.import_date is None

    print("\nAll ProductData contract assertions passed.")
    print("All integration assertions passed.")


if __name__ == "__main__":
    main()