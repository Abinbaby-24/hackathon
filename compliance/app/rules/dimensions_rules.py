import re


def check_dimensions(product):
    """
    Validates dimensional information of a packaged commodity.

    Dimensions are checked only when dimensional information
    is applicable/provided.

    Checks:
    1. Dimensions are present when applicable.
    2. Numeric dimension values are valid.
    3. Dimension values are greater than zero.
    4. Units can be identified.
    """

    checks = {}
    violations = []

    length = product.get("length")
    width = product.get("width")
    height = product.get("height")

    dimensions_applicable = product.get("dimensions_applicable")

    # --------------------------------------------------
    # 1. Check applicability
    # --------------------------------------------------

    if dimensions_applicable is False:

        checks["dimensions_applicable"] = "NOT_APPLICABLE"

        return {
            "checks": checks,
            "violations": violations
        }

    # --------------------------------------------------
    # 2. Check whether dimensions were provided
    # --------------------------------------------------

    dimensions = {
        "length": length,
        "width": width,
        "height": height
    }

    provided_dimensions = {
        key: value
        for key, value in dimensions.items()
        if value is not None and str(value).strip() != ""
    }

    if not provided_dimensions:

        checks["dimensions_present"] = "REVIEW"

        violations.append({
            "field": "dimensions",
            "message": (
                "Dimensional information was not detected. "
                "Applicability requires review."
            )
        })

        return {
            "checks": checks,
            "violations": violations
        }

    checks["dimensions_present"] = "PASS"

    # --------------------------------------------------
    # 3. Validate individual dimensions
    # --------------------------------------------------

    for dimension_name, dimension_value in provided_dimensions.items():

        number_match = re.search(
            r"\d+(?:\.\d+)?",
            str(dimension_value)
        )

        if not number_match:

            checks[f"{dimension_name}_value"] = "FAIL"

            violations.append({
                "field": dimension_name,
                "message": (
                    f"{dimension_name.capitalize()} "
                    "does not contain a valid numeric value."
                )
            })

            continue

        value = float(number_match.group())

        if value <= 0:

            checks[f"{dimension_name}_value"] = "FAIL"

            violations.append({
                "field": dimension_name,
                "message": (
                    f"{dimension_name.capitalize()} "
                    "must be greater than zero."
                )
            })

        else:

            checks[f"{dimension_name}_value"] = "PASS"

        # --------------------------------------------------
        # Check unit
        # --------------------------------------------------

        dimension_text = str(dimension_value).lower()

        units = [
            "mm",
            "cm",
            "m",
            "inch",
            "in"
        ]

        unit_found = any(
            re.search(
                r"\b" + re.escape(unit) + r"\b",
                dimension_text
            )
            for unit in units
        )

        if unit_found:

            checks[f"{dimension_name}_unit"] = "PASS"

        else:

            checks[f"{dimension_name}_unit"] = "REVIEW"

            violations.append({
                "field": dimension_name,
                "message": (
                    f"Unit for {dimension_name} "
                    "could not be identified."
                )
            })

    return {
        "checks": checks,
        "violations": violations
    }