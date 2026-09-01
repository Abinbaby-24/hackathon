from pathlib import Path

import cv2

from app.preprocessing.resize import resize_image
from app.preprocessing.enhance import enhance_image
from app.preprocessing.orientation import rotate_image


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_IMAGE = PROJECT_ROOT / "test_images" / "chips.jpeg"
OUTPUT_DIR = PROJECT_ROOT / "test_images" / "processed"


def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Input image: {INPUT_IMAGE}")

    # --------------------------------------------------
    # Load image
    # --------------------------------------------------

    image = cv2.imread(str(INPUT_IMAGE))

    if image is None:
        print("ERROR: Could not load image.")
        return

    height, width = image.shape[:2]

    print(f"Original size: {width} x {height}")

    # --------------------------------------------------
    # 1. Resize
    # --------------------------------------------------

    resized = resize_image(image, target_width=1600)

    cv2.imwrite(
        str(OUTPUT_DIR / "chips_resized.jpg"),
        resized
    )

    h, w = resized.shape[:2]

    print(f"Resized size:  {w} x {h}")

    # --------------------------------------------------
    # 2. Orientation
    # --------------------------------------------------

    rotated = rotate_image(image, 0)

    cv2.imwrite(
        str(OUTPUT_DIR / "chips_orientation.jpg"),
        rotated
    )

    print("Orientation test: 0 degrees")

    # --------------------------------------------------
    # 3. Enhancement
    # --------------------------------------------------

    enhanced = enhance_image(image)

    cv2.imwrite(
        str(OUTPUT_DIR / "chips_enhanced.jpg"),
        enhanced
    )

    h, w = enhanced.shape[:2]

    print(f"Enhanced size:  {w} x {h}")

    print("\nPreprocessing test completed.")


if __name__ == "__main__":
    main()