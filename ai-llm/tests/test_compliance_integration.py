import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OCR_PROJECT = PROJECT_ROOT / "ocr-cv"
COMPLIANCE_PROJECT = PROJECT_ROOT / "compliance"
IMAGE_PATH = PROJECT_ROOT / "test_images" / "product.jpeg"


def run_ocr():
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

    output = result.stdout
    json_start = output.find("{")

    if json_start == -1:
        raise RuntimeError(
            f"Could not find OCR JSON output.\\n{output}"
        )

    return json.loads(output[json_start:])


def run_compliance(product_data):
    code = f"""
from app.engine.validator import validate_product
import json

product = json.loads(r'''{json.dumps(product_data)}''')

result = validate_product(product)

print(json.dumps(result, ensure_ascii=False))
"""

    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=COMPLIANCE_PROJECT,
        capture_output=True,
        text=True,
        check=True,
    )

    output = result.stdout
    json_start = output.find("{")

    if json_start == -1:
        raise RuntimeError(
            f"Could not find compliance JSON output.\\n{output}"
        )

    return json.loads(output[json_start:])


def main():
    print("Running Member 2 OCR...")

    ocr_result = run_ocr()

    print(
        f"OCR regions detected: "
        f"{len(ocr_result['regions'])}"
    )

    print("\nRunning Member 3 AI extraction...")

    from app.llm_service import extract_product

    product = extract_product(ocr_result)

    product_data = product.model_dump()

    print("\nPRODUCT DATA:")
    print(product.model_dump_json(indent=2))

    print("\nRunning Member 4 compliance validation...")

    compliance_result = run_compliance(product_data)

    print("\nCOMPLIANCE RESULT:")
    print(
        json.dumps(
            compliance_result,
            indent=2,
            ensure_ascii=False
        )
    )


if __name__ == "__main__":
    main()