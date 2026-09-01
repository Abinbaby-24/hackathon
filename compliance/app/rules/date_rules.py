from datetime import datetime


def check_dates(product):
    """
    Validates date-related declarations extracted from a package.

    Checks:
    1. Manufacturing / packing / import date
    2. Best-before / use-by date when applicable
    3. Valid date format
    4. Logical relationship between production and expiry dates
    """

    checks = {}
    violations = []

    manufacturing_date = product.get("manufacturing_date")
    packing_date = product.get("packing_date")
    import_date = product.get("import_date")

    best_before = product.get("best_before")
    use_by = product.get("use_by")

    # --------------------------------------------------
    # 1. Manufacturing / Packing / Import Date
    # --------------------------------------------------

    production_date = (
        manufacturing_date
        or packing_date
        or import_date
    )

    if production_date:

        if _valid_date_format(production_date):

            checks["production_date"] = "PASS"

        else:

            checks["production_date"] = "FAIL"

            violations.append({
                "field": "production_date",
                "message": (
                    "Manufacturing, packing or import date "
                    "could not be interpreted as a valid date."
                )
            })

    else:

        checks["production_date"] = "REVIEW"

        violations.append({
            "field": "production_date",
            "message": (
                "Manufacturing, packing or import date "
                "was not detected."
            )
        })

    # --------------------------------------------------
    # 2. Best-before / Use-by
    # --------------------------------------------------

    if best_before:

        if _valid_date_format(best_before):

            checks["best_before"] = "PASS"

        else:

            checks["best_before"] = "FAIL"

            violations.append({
                "field": "best_before",
                "message": (
                    "Best-before date could not be "
                    "interpreted as a valid date."
                )
            })

    elif use_by:

        if _valid_date_format(use_by):

            checks["use_by"] = "PASS"

        else:

            checks["use_by"] = "FAIL"

            violations.append({
                "field": "use_by",
                "message": (
                    "Use-by/expiry date could not be "
                    "interpreted as a valid date."
                )
            })

    else:

        # Applicability depends on the type of commodity.
        checks["best_before_or_use_by"] = "REVIEW"

        violations.append({
            "field": "best_before_or_use_by",
            "message": (
                "No best-before or use-by declaration was detected. "
                "Applicability requires review."
            )
        })

    # --------------------------------------------------
    # 3. Logical Date Relationship
    # --------------------------------------------------

    end_date = best_before or use_by

    if production_date and end_date:

        production = _parse_date(production_date)
        expiry = _parse_date(end_date)

        if production and expiry:

            if expiry > production:

                checks["date_order"] = "PASS"

            else:

                checks["date_order"] = "FAIL"

                violations.append({
                    "field": "dates",
                    "message": (
                        "Best-before/use-by date must be later "
                        "than the manufacturing/packing/import date."
                    )
                })

        else:

            checks["date_order"] = "REVIEW"

    # --------------------------------------------------
    # 4. Return result
    # --------------------------------------------------

    return {
        "checks": checks,
        "violations": violations
    }


def _valid_date_format(date_value):
    """
    Checks whether the extracted date can be interpreted.
    """

    return _parse_date(date_value) is not None


def _parse_date(date_value):
    """
    Converts supported OCR/AI date formats into datetime.

    Supports both complete dates and month/year formats.
    """

    if not date_value:
        return None

    date_text = str(date_value).strip()

    formats = [
        # Complete dates
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%d.%m.%Y",

        # Month + year
        "%Y-%m",
        "%m-%Y",
        "%m/%Y",
        "%B %Y",
        "%b %Y"
    ]

    for date_format in formats:

        try:
            return datetime.strptime(
                date_text,
                date_format
            )

        except ValueError:
            continue

    return None