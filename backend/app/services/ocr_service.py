import importlib.util
import sys
from pathlib import Path


OCR_ROOT = (
    Path(__file__).resolve().parents[2] / ".." / "ocr-cv"
).resolve()


def _load_ocr_pipeline():
    """
    Load OCRPipeline from the separate ocr-cv project
    without conflicting with the backend's app package.
    """

    package_name = "ocr_cv"

    if package_name not in sys.modules:
        package = importlib.util.module_from_spec(
            importlib.util.spec_from_loader(
                package_name,
                loader=None,
                is_package=True
            )
        )

        package.__path__ = [
            str(OCR_ROOT / "app")
        ]

        sys.modules[package_name] = package

    module_name = "ocr_cv.pipeline"
    pipeline_path = OCR_ROOT / "app" / "pipeline.py"

    spec = importlib.util.spec_from_file_location(
        module_name,
        pipeline_path,
        submodule_search_locations=[]
    )

    module = importlib.util.module_from_spec(spec)

    sys.modules[module_name] = module

    spec.loader.exec_module(module)

    return module.OCRPipeline


def process_image(image_path):
    """
    Process an image using the OCR-CV pipeline.
    """

    OCRPipeline = _load_ocr_pipeline()

    pipeline = OCRPipeline(
        resize=True,
        enhance=True,
        rotation=0
    )

    return pipeline.process(image_path)