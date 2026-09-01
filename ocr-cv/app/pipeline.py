from pathlib import Path

import cv2

from .ocr.paddle_ocr import OCRProcessor
from .preprocessing.resize import resize_image
from .preprocessing.orientation import rotate_image
from .preprocessing.enhance import enhance_image


class OCRPipeline:
    """
    Complete OCR-CV pipeline.

    Flow:
        Image
        -> Optional preprocessing
        -> PaddleOCR
        -> Structured OCR result
    """

    def __init__(
        self,
        resize=False,
        enhance=False,
        rotation=0
    ):
        self.use_resize = resize
        self.use_enhance = enhance
        self.rotation = rotation

        self.ocr = OCRProcessor()

    def preprocess(self, image):
        """
        Apply the selected preprocessing operations.
        """

        processed = image

        # Resize
        if self.use_resize:
            processed = resize_image(
                processed,
                target_width=1600
            )

        # Rotation
        if self.rotation != 0:
            processed = rotate_image(
                processed,
                self.rotation
            )

        # Enhancement
        if self.use_enhance:
            processed = enhance_image(processed)

        return processed

    def process(self, image_path):
        """
        Run the complete OCR pipeline.

        Args:
            image_path: Path to input image.

        Returns:
            Structured OCR result.
        """

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        # Load image
        image = cv2.imread(str(image_path))

        if image is None:
            raise ValueError(
                f"Could not read image: {image_path}"
            )

        # Preprocess
        processed_image = self.preprocess(image)

        # Save temporary processed image
        temp_path = image_path.parent / "_ocr_temp.jpg"

        success = cv2.imwrite(
            str(temp_path),
            processed_image
        )

        if not success:
            raise RuntimeError(
                "Failed to save temporary processed image."
            )

        try:
            # Run OCR
            result = self.ocr.extract(temp_path)

        finally:
            # Always remove temporary image
            if temp_path.exists():
                temp_path.unlink()

        return result
