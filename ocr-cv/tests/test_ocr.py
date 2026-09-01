from pathlib import Path

from app.ocr.paddle_ocr import OCRProcessor


PROJECT_ROOT = Path(__file__).resolve().parents[1]

IMAGE_PATH = PROJECT_ROOT / "test_images" / "chips.jpeg"


def main():
    print(f"Image: {IMAGE_PATH}")

    if not IMAGE_PATH.exists():
        print("ERROR: Image not found.")
        return

    ocr = OCRProcessor()

    print("\nRunning OCR...\n")

    result = ocr.extract(IMAGE_PATH)

    print("========================================")
    print("FULL TEXT")
    print("========================================")
    print(result["text"])

    print("\n========================================")
    print("OCR REGIONS")
    print("========================================")

    for region in result["regions"]:
        print(f"\nText       : {region['text']}")
        print(f"Confidence : {region['confidence']:.4f}")
        print(f"Box        : {region['box']}")

    print("\n========================================")
    print(f"Total regions: {len(result['regions'])}")
    print("========================================")


if __name__ == "__main__":
    main()