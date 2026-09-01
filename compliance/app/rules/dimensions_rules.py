import re


def check_dimensions(product):
    """
    Validates dimensional information of a packaged commodity.

    Dimensions are checked only when they are explicitly marked
    as applicable or when dimensional information is provided.

    Checks:
    1. Dimensions are applicable.
    2. Dimension values contain valid numbers.
    3. Dimension values are greater than zero.
    4. Dimension units can be identified.
    """

    checks = {}
    violations = []

    length = product.get("length")
    width = product.get("width")
    height = product.get("height")

    dimensions_applicable = product.get("dimensions_applicable")

    # --------------------------------------------------
    # 1. Determine applicability
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

    # Explicitly marked as not applicable
    if dimensions_applicable is False:

        checks["dimensions_applicable"] = "NOT_APPLICABLE"

        return {
            "checks": checks,
            "violations": violations
        }

    # No dimensional information and applicability unknown.
    # Do not assume that dimensions are required.
    if not provided_dimensions and dimensions_applicable is not True:

        checks["dimensions_applicable"] = "NOT_APPLICABLE"

        return {
            "checks": checks,
            "violations": violations
        }

    # Dimensions explicitly marked as applicable but missing.
    if dimensions_applicable is True and not provided_dimensions:

        checks["dimensions_applicable"] = "PASS"
        checks["dimensions_present"] = "FAIL"

        violations.append({
            "field": "dimensions",
            "message": (
                "Dimensional information is required but "
                "was not detected."
            )
        })

        return {
            "checks": checks,
            "violations": violations
        }

    # --------------------------------------------------
    # 2. Dimensions are applicable/provided
    # --------------------------------------------------

    checks["dimensions_applicable"] = "PASS"
    checks["dimensions_present"] = "PASS"

    # --------------------------------------------------
    # 3. Validate individual dimensions
    # --------------------------------------------------

    units = [
        "mm",
        "cm",
        "m",
        "inch",
        "in"
    ]

    for dimension_name, dimension_value in provided_dimensions.items():

        dimension_text = str(dimension_value).strip()

        # --------------------------------------------------
        # Numeric value
        # --------------------------------------------------

        number_match = re.search(
            r"\d+(?:\.\d+)?",
            dimension_text
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
        # Unit
        # --------------------------------------------------

        dimension_lower = dimension_text.lower()

        unit_found = False

        for unit in units:

            pattern = (
                r"(?<![a-z])"
                + re.escape(unit.lower())
                + r"(?![a-z])"
            )

            if re.search(pattern, dimension_lower):
                unit_found = True
                break

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