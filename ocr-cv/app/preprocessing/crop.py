import cv2


def crop_image(image, x1, y1, x2, y2):
    """
    Crop an image using pixel coordinates.

    Args:
        image: OpenCV image
        x1, y1: Top-left corner
        x2, y2: Bottom-right corner

    Returns:
        Cropped image
    """

    height, width = image.shape[:2]

    x1 = max(0, min(x1, width))
    x2 = max(0, min(x2, width))
    y1 = max(0, min(y1, height))
    y2 = max(0, min(y2, height))

    if x1 >= x2 or y1 >= y2:
        raise ValueError("Invalid crop coordinates.")

    return image[y1:y2, x1:x2]