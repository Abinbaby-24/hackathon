import os
import shutil
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException



from app.services.ocr_service import process_image
from app.services.ai_service import extract_product_data
from app.services.compliance_service import check_compliance

from app.database.queries import (
    create_product,
    create_inspection,
    create_violation
)


router = APIRouter(
    prefix="/scan",
    tags=["Scan"]
)


@router.post("/")
async def scan_product(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No image selected"
        )

    temp_filename = None

    try:
        # -----------------------------
        # 1. Save temporary image
        # -----------------------------

        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_filename = temp_file.name

            shutil.copyfileobj(
                file.file,
                temp_file
            )

        # -----------------------------
        # 2. OCR
        # -----------------------------

        ocr_result = process_image(temp_filename)

        # -----------------------------
        # 3. AI extraction
        # -----------------------------

        product_data = extract_product_data(
            ocr_result
        )

        # -----------------------------
        # 4. Compliance
        # -----------------------------

        compliance_result = check_compliance(
            product_data
        )

        # -----------------------------
        # 5. Save product
        # -----------------------------

        product = create_product(product_data)

        if not product:
            raise HTTPException(
                status_code=500,
                detail="Failed to save product"
            )

        # -----------------------------
        # 6. Save inspection
        # -----------------------------

        inspection_data = {
            "product_id": product["id"],
            "score": compliance_result["score"],
            "status": compliance_result["status"]
        }

        inspection = create_inspection(
            inspection_data
        )

        if not inspection:
            raise HTTPException(
                status_code=500,
                detail="Failed to save inspection"
            )

        # -----------------------------
        # 7. Save violations
        # -----------------------------

        for violation in compliance_result.get(
            "violations",
            []
        ):

            violation_data = {
                **violation,
                "inspection_id": inspection["id"]
            }

            create_violation(
                violation_data
            )

        # -----------------------------
        # 8. Return result
        # -----------------------------

        return {
            "inspection_id": inspection["id"],
            "product": product_data,
            "compliance": compliance_result,
            "ocr": ocr_result
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        # -----------------------------
        # 9. Delete temporary image
        # -----------------------------

        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)


