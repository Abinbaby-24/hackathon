import re


def check_standard_pack(product):
    """
    Validates standard-pack information available from the
    extracted product data.

    The rule performs generic validation of quantity and unit.
    Commodity-specific standard pack sizes are checked only
    when a standard_pack_size value is supplied in the product data.
    """

    checks = {}
    violations = []

    quantity = product.get("net_quantity")

    # --------------------------------------------------
    # 1. Quantity presence
    # --------------------------------------------------

    if not quantity:
        checks["standard_pack_quantity"] = "FAIL"

        violations.append({
            "field": "net_quantity",
            "message": (
                "Net quantity is required to verify "
                "standard pack information."
            )
        })

        return {
            "checks": checks,
            "violations": violations
        }

    checks["standard_pack_quantity"] = "PASS"

    quantity_text = str(quantity).strip().lower()

    # --------------------------------------------------
    # 2. Numeric quantity
    # --------------------------------------------------

    number_match = re.search(
        r"\d+(?:\.\d+)?",
        quantity_text
    )

    if not number_match:

        checks["standard_pack_value"] = "FAIL"

        violations.append({
            "field": "net_quantity",
            "message": (
                "A numeric quantity value could not "
                "be identified."
            )
        })

    else:

        value = float(number_match.group())

        if value > 0:

            checks["standard_pack_value"] = "PASS"

        else:

            checks["standard_pack_value"] = "FAIL"

            violations.append({
                "field": "net_quantity",
                "message": (
                    "Standard pack quantity must be "
                    "greater than zero."
                )
            })

    # --------------------------------------------------
    # 3. Standard measurement unit
    # --------------------------------------------------

    recognized_units = [
        "kg",
        "g",
        "mg",
        "l",
        "ml",
        "litre",
        "liter",
        "m",
        "cm",
        "mm",
        "metre",
        "meter",
        "pcs",
        "piece",
        "pieces",
        "number",
        "nos"
    ]

    unit_found = any(
        re.search(
            r"\b" + re.escape(unit) + r"\b",
            quantity_text
        )
        for unit in recognized_units
    )

    if unit_found:

        checks["standard_unit"] = "PASS"

    else:

        checks["standard_unit"] = "FAIL"

        violations.append({
            "field": "net_quantity",
            "message": (
                "The declared quantity does not "
                "contain a recognized standard unit."
            )
        })

    # --------------------------------------------------
    # 4. Commodity-specific standard pack size
    # --------------------------------------------------

    required_pack_size = product.get("standard_pack_size")

    if required_pack_size is None:

        # Current ProductData does not provide enough
        # information to perform commodity-specific
        # pack-size comparison.
        checks["commodity_specific_pack_size"] = "NOT_APPLICABLE"

    else:

        try:
            required_value = float(required_pack_size)

            if number_match:

                declared_value = float(number_match.group())

                if declared_value == required_value:

                    checks["commodity_specific_pack_size"] = "PASS"

                else:

                    checks["commodity_specific_pack_size"] = "FAIL"

                    violations.append({
                        "field": "standard_pack_size",
                        "message": (
                            "Declared pack size does not match "
                            "the required standard pack size."
                        )
                    })

            else:

                checks["commodity_specific_pack_size"] = "REVIEW"

        except (ValueError, TypeError):

            checks["commodity_specific_pack_size"] = "REVIEW"

            violations.append({
                "field": "standard_pack_size",
                "message": (
                    "The required standard pack size "
                    "could not be interpreted."
                )
            })

    return {
        "checks": checks,
        "violations": violations
    }