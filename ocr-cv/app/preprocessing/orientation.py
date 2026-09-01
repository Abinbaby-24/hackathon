import cv2


def rotate_image(image, angle):
    """
    Rotate image by 90-degree increments.

    Args:
        image: OpenCV image
        angle: 0, 90, 180, or 270

    Returns:
        Rotated image
    """

    if angle == 0:
        return image

    if angle == 90:
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    if angle == 180:
        return cv2.rotate(image, cv2.ROTATE_180)

    if angle == 270:
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    raise ValueError(
        "Angle must be 0, 90, 180, or 270"
    )