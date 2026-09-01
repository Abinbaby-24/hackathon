from pathlib import Path

from app.pipeline import OCRPipeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]

IMAGE_PATH = PROJECT_ROOT / "test_images" / "chips.jpeg"


def run_test(name, resize=False, enhance=False, rotation=0):
    """
    Run OCR pipeline with a specific preprocessing configuration.
    """

    print("\n")
    print("=" * 70)
    print(f"TEST: {name}")
    print("=" * 70)

    print(f"Resize    : {resize}")
    print(f"Enhance   : {enhance}")
    print(f"Rotation  : {rotation}")
    print(f"Image     : {IMAGE_PATH}")

    try:
        pipeline = OCRPipeline(
            resize=resize,
            enhance=enhance,
            rotation=rotation
        )

        result = pipeline.process(IMAGE_PATH)

        print("\nOCR completed successfully.")

        print(f"Detected regions: {len(result['regions'])}")

        print("\nDetected text:")

        for region in result["regions"]:
            print(
                f"- {region['text']} "
                f"| confidence={region['confidence']:.4f} "
                f"| box={region['box']}"
            )

        return result

    except Exception as e:
        print("\nERROR:")
        print(e)
        return None


def main():

    print("=" * 70)
    print("OCR PIPELINE PREPROCESSING COMPARISON")
    print("=" * 70)

    if not IMAGE_PATH.exists():
        print(f"\nERROR: Image not found:")
        print(IMAGE_PATH)
        return

    # --------------------------------------------------
    # TEST 1 — BASELINE
    # No preprocessing
    # --------------------------------------------------

    baseline = run_test(
        name="BASELINE",
        resize=False,
        enhance=False,
        rotation=0
    )

    # --------------------------------------------------
    # TEST 2 — RESIZE
    # --------------------------------------------------

    resized = run_test(
        name="RESIZE ONLY",
        resize=True,
        enhance=False,
        rotation=0
    )

    # --------------------------------------------------
    # TEST 3 — ENHANCEMENT
    # --------------------------------------------------

    enhanced = run_test(
        name="ENHANCEMENT ONLY",
        resize=False,
        enhance=True,
        rotation=0
    )

    # --------------------------------------------------
    # TEST 4 — RESIZE + ENHANCEMENT
    # --------------------------------------------------

    resized_enhanced = run_test(
        name="RESIZE + ENHANCEMENT",
        resize=True,
        enhance=True,
        rotation=0
    )

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    print("\n")
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    tests = [
        ("Baseline", baseline),
        ("Resize", resized),
        ("Enhancement", enhanced),
        ("Resize + Enhancement", resized_enhanced),
    ]

    for name, result in tests:

        if result is None:
            print(f"{name:<25}: FAILED")
        else:
            regions = len(result["regions"])

            if regions > 0:
                avg_confidence = (
                    sum(
                        region["confidence"]
                        for region in result["regions"]
                    )
                    / regions
                )
            else:
                avg_confidence = 0

            print(
                f"{name:<25}: "
                f"{regions} regions | "
                f"average confidence = {avg_confidence:.4f}"
            )


if __name__ == "__main__":
    main()