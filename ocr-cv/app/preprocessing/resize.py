import cv2


def resize_image(image, target_width=1600):
    """
    Resize image while maintaining aspect ratio.

    Args:
        image: OpenCV image (NumPy array)
        target_width: Desired width in pixels

    Returns:
        Resized OpenCV image
    """

    height, width = image.shape[:2]

    if width == target_width:
        return image

    scale = target_width / width

    new_width = int(width * scale)
    new_height = int(height * scale)

    resized = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_CUBIC
    )

    return resized