from pathlib import Path

from app.ocr.paddle_ocr import OCRProcessor


PROJECT_ROOT = Path(__file__).resolve().parents[1]

IMAGE_DIR = PROJECT_ROOT / "test_images"

IMAGES = {
    "Original": IMAGE_DIR / "chips.jpeg",
    "Resized": IMAGE_DIR / "processed" / "chips_resized.jpg",
    "Enhanced": IMAGE_DIR / "processed" / "chips_enhanced.jpg",
}


def main():

    ocr = OCRProcessor()

    print("=" * 60)
    print("OCR PREPROCESSING COMPARISON")
    print("=" * 60)

    for name, image_path in IMAGES.items():

        print(f"\n{'=' * 60}")
        print(f"{name}")
        print(f"Image: {image_path}")
        print(f"{'=' * 60}")

        if not image_path.exists():
            print("ERROR: Image not found.")
            continue

        result = ocr.extract(image_path)

        print(f"Detected regions: {len(result['regions'])}")

        print("\nDetected text:")

        for region in result["regions"]:
            print(
                f"- {region['text']} "
                f"(confidence={region['confidence']:.4f})"
            )


if __name__ == "__main__":
    main()