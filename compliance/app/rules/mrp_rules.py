def check_mrp(product):
    """
    Validates the Maximum Retail Price (MRP)
    of a packaged commodity.

    Checks:
    1. MRP is present
    2. MRP is a valid positive number
    3. Selling price does not exceed MRP, if available
    4. MRP is inclusive of applicable taxes
    """

    checks = {}
    violations = []

    mrp = product.get("mrp")
    selling_price = product.get("selling_price")

    # --------------------------------------------------
    # 1. Check whether MRP is present
    # --------------------------------------------------

    if mrp is None or str(mrp).strip() == "":
        checks["mrp_present"] = "FAIL"

        violations.append({
            "field": "mrp",
            "message": (
                "Maximum Retail Price (MRP) is missing."
            )
        })

        return {
            "checks": checks,
            "violations": violations
        }

    checks["mrp_present"] = "PASS"

    # --------------------------------------------------
    # 2. Check that MRP is a valid positive number
    # --------------------------------------------------

    try:

        mrp_value = float(mrp)

        if mrp_value <= 0:

            checks["mrp_value"] = "FAIL"

            violations.append({
                "field": "mrp",
                "message": (
                    "MRP must be greater than zero."
                )
            })

            return {
                "checks": checks,
                "violations": violations
            }

        else:

            checks["mrp_value"] = "PASS"

    except (ValueError, TypeError):

        checks["mrp_value"] = "FAIL"

        violations.append({
            "field": "mrp",
            "message": (
                "MRP must be a valid numeric value."
            )
        })

        return {
            "checks": checks,
            "violations": violations
        }

    # --------------------------------------------------
    # 3. Check selling price against MRP
    # --------------------------------------------------

    if selling_price is not None and str(selling_price).strip() != "":

        try:

            selling_price_value = float(selling_price)

            if selling_price_value < 0:

                checks["selling_price"] = "FAIL"

                violations.append({
                    "field": "selling_price",
                    "message": (
                        "Selling price cannot be negative."
                    )
                })

            elif selling_price_value > mrp_value:

                checks["selling_price"] = "FAIL"

                violations.append({
                    "field": "selling_price",
                    "message": (
                        "Selling price must not exceed the declared MRP."
                    )
                })

            else:

                checks["selling_price"] = "PASS"

        except (ValueError, TypeError):

            checks["selling_price"] = "REVIEW"

            violations.append({
                "field": "selling_price",
                "message": (
                    "Selling price could not be verified."
                )
            })

    else:

        checks["selling_price"] = "NOT_APPLICABLE"

    # --------------------------------------------------
    # 4. MRP should be inclusive of applicable taxes
    # --------------------------------------------------

    tax_inclusion = product.get("mrp_inclusive_of_taxes")

    if tax_inclusion is True:

        checks["tax_inclusion"] = "PASS"

    elif tax_inclusion is False:

        checks["tax_inclusion"] = "FAIL"

        violations.append({
            "field": "mrp_inclusive_of_taxes",
            "message": (
                "Declared MRP should be inclusive of all applicable taxes."
            )
        })

    else:

        checks["tax_inclusion"] = "REVIEW"

        violations.append({
            "field": "mrp_inclusive_of_taxes",
            "message": (
                "Could not verify whether the declared MRP "
                "is inclusive of applicable taxes."
            )
        })

    return {
        "checks": checks,
        "violations": violations
    }