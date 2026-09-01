from pathlib import Path

from app.llm_service import extract_product


def run_test(filename: str):
    ocr_file = Path("tests") / filename
    ocr_text = ocr_file.read_text(encoding="utf-8")

    # Simulate Member 2's OCR output
    ocr_result = {
        "text": ocr_text,
        "regions": []
    }

    result = extract_product(ocr_result)

    print(f"\n--- {filename} ---")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    run_test("sample_ocr_final_format.txt")
    run_test("sample_ocr_missing_final.txt")