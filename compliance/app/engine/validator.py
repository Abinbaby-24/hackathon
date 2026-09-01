from app.rules.mandatory_declarations import check_mandatory_declarations
from app.rules.mrp_rules import check_mrp
from app.rules.quantity_rules import check_quantity
from app.rules.date_rules import check_dates
from app.rules.dimensions_rules import check_dimensions
from app.rules.display_panel_rules import check_display_panel
from app.rules.standard_pack_rules import check_standard_pack

from app.engine.scorer import calculate_score
from app.engine.status import determine_status


def validate_product(product):
    """
    Runs all available Legal Metrology compliance checks
    and returns the final inspection result.

    Current checks:
    - Mandatory declarations
    - MRP
    - Net quantity
    - Date declarations
    - Dimensions
    - Display panel
    - Standard pack size
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
    # 5. Dimensions Rules
    # --------------------------------------------------

    dimensions_result = check_dimensions(product)

    all_checks["dimensions"] = dimensions_result["checks"]

    all_violations.extend(
        dimensions_result["violations"]
    )

    # --------------------------------------------------
    # 6. Display Panel Rules
    # --------------------------------------------------

    display_panel_result = check_display_panel(product)

    all_checks["display_panel"] = (
        display_panel_result["checks"]
    )

    all_violations.extend(
        display_panel_result["violations"]
    )

    # --------------------------------------------------
    # 7. Standard Pack Size Rules
    # --------------------------------------------------

    standard_pack_result = check_standard_pack(product)

    all_checks["standard_pack_size"] = (
        standard_pack_result["checks"]
    )

    all_violations.extend(
        standard_pack_result["violations"]
    )

    # --------------------------------------------------
    # 8. Calculate Compliance Score
    # --------------------------------------------------

    score_data = calculate_score(all_checks)

    # --------------------------------------------------
    # 9. Determine Final Status
    # --------------------------------------------------

    status = determine_status(
        score_data,
        all_violations
    )

    # --------------------------------------------------
    # 10. Return Final Compliance Result
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