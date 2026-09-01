from pathlib import Path

from paddleocr import PaddleOCR


class OCRProcessor:
    """
    PaddleOCR wrapper for the OCR-CV module.

    Returns:
        text
        confidence
        bounding boxes
    """

    def __init__(self):
        self.ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            enable_mkldnn=False,
        )

    def extract(self, image_path):
        """
        Run OCR on an image and return the agreed OCR JSON structure.
        """

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        results = list(self.ocr.predict(str(image_path)))

        if not results:
            return {
                "text": "",
                "regions": []
            }

        result = results[0]

        # PaddleOCR 3.x result object
        result_json = result.json

        # The JSON representation contains the actual OCR data
        data = result_json.get("res", {})

        texts = data.get("rec_texts", [])
        scores = data.get("rec_scores", [])
        boxes = data.get("rec_boxes", [])

        regions = []
        all_text = []

        for text, score, box in zip(texts, scores, boxes):

            text = str(text).strip()

            if not text:
                continue

            confidence = float(score)

            box = [int(value) for value in box]

            all_text.append(text)

            regions.append({
                "text": text,
                "confidence": confidence,
                "box": box
            })

        return {
            "text": " ".join(all_text),
            "regions": regions
        }