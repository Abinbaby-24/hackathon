from app.rules.mandatory_declarations import check_mandatory_declarations
from app.rules.mrp_rules import check_mrp
from app.rules.quantity_rules import check_quantity
from app.rules.date_rules import check_dates
from app.rules.standard_pack_rules import check_standard_pack
from app.rules.display_panel_rules import check_display_panel

from app.engine.scorer import calculate_score
from app.engine.status import determine_status


def _normalize_product(product):
    """
    Converts Member 3's ProductData field names into the
    field names expected by the compliance rules.
    """

    normalized = dict(product)

    # Member 3 -> Compliance field mapping
    if not normalized.get("manufacturer_packer_importer"):
        normalized["manufacturer_packer_importer"] = (
            normalized.get("manufacturer")
        )

    if not normalized.get("manufacturing_date"):
        normalized["manufacturing_date"] = (
            normalized.get("packing_date")
        )

    if not normalized.get("consumer_care_details"):
        normalized["consumer_care_details"] = (
            normalized.get("consumer_care")
        )

    # Determine imported status
    if "is_imported" not in normalized:
        normalized["is_imported"] = bool(
            normalized.get("country_of_origin")
        )

    # Optional fields
    normalized.setdefault("selling_price", None)
    normalized.setdefault("mrp_inclusive_of_taxes", None)
    normalized.setdefault("unit_sale_price", None)

    return normalized


def validate_product(product, ocr_result=None):
    """
    Runs all available Legal Metrology compliance checks.

    Args:
        product: Product data extracted by the AI/LLM module.
        ocr_result: Optional OCR result from Member 2.

    Returns:
        Complete compliance inspection result.
    """

    if not isinstance(product, dict):

        return {
            "status": "REVIEW",
            "score": 0,
            "statistics": {
                "total_checks": 0,
                "passed": 0,
                "review": 1,
                "failed": 0
            },
            "checks": {},
            "violations": [
                {
                    "field": "product",
                    "message": (
                        "Product data could not be interpreted "
                        "as a valid object."
                    )
                }
            ]
        }

    # Normalize Member 3's output
    product = _normalize_product(product)

    all_checks = {}
    all_violations = []

    # --------------------------------------------------
    # 1. Mandatory Declarations
    # --------------------------------------------------

    declaration_result = check_mandatory_declarations(product)

    all_checks["mandatory_declarations"] = (
        declaration_result["checks"]
    )

    all_violations.extend(
        declaration_result["violations"]
    )

    # --------------------------------------------------
    # 2. MRP Rules
    # --------------------------------------------------

    mrp_result = check_mrp(product)

    all_checks["mrp"] = mrp_result["checks"]

    all_violations.extend(
        mrp_result["violations"]
    )

    # --------------------------------------------------
    # 3. Quantity Rules
    # --------------------------------------------------

    quantity_result = check_quantity(product)

    all_checks["quantity"] = quantity_result["checks"]

    all_violations.extend(
        quantity_result["violations"]
    )

    # --------------------------------------------------
    # 4. Date Rules
    # --------------------------------------------------

    date_result = check_dates(product)

    all_checks["dates"] = date_result["checks"]

    all_violations.extend(
        date_result["violations"]
    )

    # --------------------------------------------------
    # 5. Standard Pack Rules
    # --------------------------------------------------

    standard_pack_result = check_standard_pack(product)

    all_checks["standard_pack"] = (
        standard_pack_result["checks"]
    )

    all_violations.extend(
        standard_pack_result["violations"]
    )

    # --------------------------------------------------
    # 6. Display Panel Rules
    # --------------------------------------------------

    # Use OCR passed directly to the validator.
    # If it is not provided, display-panel OCR checking
    # is not applicable for this validation.

    if ocr_result:

        display_result = check_display_panel(
            ocr_result,
            product
        )

        all_checks["display_panel"] = (
            display_result["checks"]
        )

        all_violations.extend(
            display_result["violations"]
        )

    else:

        all_checks["display_panel"] = {
            "display_panel_ocr": "NOT_APPLICABLE"
        }

    # --------------------------------------------------
    # 7. Calculate Compliance Score
    # --------------------------------------------------

    score_data = calculate_score(all_checks)

    # --------------------------------------------------
    # 8. Determine Final Status
    # --------------------------------------------------

    status = determine_status(
        score_data,
        all_violations
    )

    # --------------------------------------------------
    # 9. Return Final Compliance Result
    # --------------------------------------------------

    return {
        "status": status,
        "score": score_data["score"],
        "statistics": {
            "total_checks": score_data["total_checks"],
            "passed": score_data["passed"],
            "review": score_data["review"],
            "failed": score_data["failed"]
        },
        "checks": all_checks,
        "violations": all_violations
    }