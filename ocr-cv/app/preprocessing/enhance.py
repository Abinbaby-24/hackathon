import cv2


def enhance_image(image):
    """
    Enhance image for OCR.

    Uses grayscale conversion and CLAHE
    for local contrast enhancement.

    Args:
        image: OpenCV BGR image

    Returns:
        Enhanced grayscale image
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    return enhanced