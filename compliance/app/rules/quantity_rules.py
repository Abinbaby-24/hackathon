import re


def check_quantity(product):
    """
    Validates the net quantity declaration of a packaged commodity.

    Checks:
    1. Net quantity is present
    2. Numeric quantity is present
    3. Recognized net-quantity unit is present
    4. Quantity is greater than zero
    """

    checks = {}
    violations = []

    quantity = product.get("net_quantity")

    # --------------------------------------------------
    # 1. Check whether net quantity is present
    # --------------------------------------------------

    if quantity is None or str(quantity).strip() == "":
        checks["quantity_present"] = "FAIL"

        violations.append({
            "field": "net_quantity",
            "message": "Net quantity declaration is missing."
        })

        return {
            "checks": checks,
            "violations": violations
        }

    checks["quantity_present"] = "PASS"

    quantity_text = str(quantity).strip()

    # --------------------------------------------------
    # 2. Check for a numeric value
    # --------------------------------------------------

    number_match = re.search(
        r"\d+(?:\.\d+)?",
        quantity_text
    )

    if not number_match:

        checks["quantity_value"] = "FAIL"

        violations.append({
            "field": "net_quantity",
            "message": (
                "Net quantity does not contain a valid numeric value."
            )
        })

        return {
            "checks": checks,
            "violations": violations
        }

    checks["quantity_value"] = "PASS"

    # --------------------------------------------------
    # 3. Check for a recognized net-quantity unit
    # --------------------------------------------------

    recognized_units = [
        "kg",
        "g",
        "mg",
        "µg",
        "ug",

        "l",
        "litre",
        "liter",
        "ml",

        "pcs",
        "pc",
        "piece",
        "pieces",
        "number",
        "nos"
    ]

    quantity_lower = quantity_text.lower()

    unit_found = False

    for unit in recognized_units:

        # Allow units directly after numbers:
        # 200g
        # 13g
        # 1kg
        # 500ml
        #
        # Also allow separated forms:
        # 200 g
        # 1 kg
        # 500 ml
        pattern = r"(?<![a-z])" + re.escape(unit.lower()) + r"(?![a-z])"

        if re.search(pattern, quantity_lower):
            unit_found = True
            break

    if unit_found:

        checks["unit"] = "PASS"

    else:

        checks["unit"] = "REVIEW"

        violations.append({
            "field": "net_quantity",
            "message": (
                "The unit of net quantity could not be identified. "
                "Expected a recognized weight, volume or number unit."
            )
        })

    # --------------------------------------------------
    # 4. Check that quantity is greater than zero
    # --------------------------------------------------

    try:

        value = float(number_match.group())

        if value <= 0:

            checks["positive_quantity"] = "FAIL"

            violations.append({
                "field": "net_quantity",
                "message": (
                    "Net quantity must be greater than zero."
                )
            })

        else:

            checks["positive_quantity"] = "PASS"

    except ValueError:

        checks["positive_quantity"] = "REVIEW"

        violations.append({
            "field": "net_quantity",
            "message": (
                "Net quantity value could not be interpreted."
            )
        })

    return {
        "checks": checks,
        "violations": violations
    }