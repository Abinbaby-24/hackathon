from pathlib import Path

from app.llm_service import extract_product


def run_test(filename: str):
    ocr_file = Path("tests") / filename
    ocr_text = ocr_file.read_text(encoding="utf-8")

    result = extract_product(ocr_text)

    print(f"\n--- {filename} ---")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    run_test("sample_ocr_complete.txt")
    run_test("sample_ocr_missing_fields.txt")
    run_test("sample_ocr_messy.txt")