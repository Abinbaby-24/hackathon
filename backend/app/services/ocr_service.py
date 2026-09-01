def process_image(image_path):
    """
    Temporary OCR implementation.

    Member 2 will replace this implementation
    with the actual OpenCV + PaddleOCR pipeline.
    """

    return {
        "text": "ABC BISCUITS MRP ₹50 NET WT 200 g PKD 08/2026 Mfd by ABC Foods",
        "regions": [
            {
                "text": "ABC BISCUITS",
                "confidence": 0.96,
                "box": [100, 100, 300, 140]
            },
            {
                "text": "MRP ₹50",
                "confidence": 0.97,
                "box": [120, 250, 240, 280]
            },
            {
                "text": "NET WT 200 g",
                "confidence": 0.94,
                "box": [120, 300, 280, 330]
            }
        ]
    }