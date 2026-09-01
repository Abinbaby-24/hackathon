import re
from datetime import datetime


def check_dates(product):
    """
    Validates date-related declarations extracted from a package.

    Checks:
    1. Manufacturing / packing / import date
    2. Best-before / use-by date when applicable
    3. Valid date format or recognized relative declaration
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

        elif _is_relative_best_before(best_before):

            checks["best_before"] = "PASS"

        else:

            checks["best_before"] = "FAIL"

            violations.append({
                "field": "best_before",
                "message": (
                    "Best-before date could not be "
                    "interpreted as a valid date or "
                    "recognized relative declaration."
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

    # Only compare actual calendar dates.
    #
    # A relative best-before declaration such as
    # "6 months from the date of packing" is not itself
    # a calendar date, so it cannot be directly compared
    # here.
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

            # Relative best-before declarations cannot be
            # compared as calendar dates without calculating
            # the declaration against a relevant reference date.
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
    Checks whether the extracted date can be interpreted
    as one of the supported calendar date formats.
    """

    return _parse_date(date_value) is not None


def _is_relative_best_before(value):
    """
    Detects common relative best-before declarations.

    Examples accepted:

        6 MONTHS FROM PACKING
        6 MONTHS FROM THE DATE OF PACKING
        12 MONTHS FROM MANUFACTURE
        12 MONTHS FROM THE DATE OF MANUFACTURE
        6 MONTHS FROM THE DATE OF MFD
        BEST BEFORE 6 MONTHS FROM PACKING

    OCR may remove spaces, for example:

        SIXMONTHSFROMTHEDATEOFPA...
    """

    if not value:
        return False

    text = str(value).strip().lower()

    if not text:
        return False

    # Normalize common OCR punctuation/spaces.
    normalized = re.sub(r"[^a-z0-9]+", "", text)

    # --------------------------------------------------
    # Numeric relative declaration
    # --------------------------------------------------

    numeric_pattern = (
        r"\d+"
        r"(?:"
        r"day|days|"
        r"month|months|"
        r"year|years"
        r")"
        r"from"
        r"(?:the)?"
        r"(?:dateof)?"
        r"(?:packing|packed|manufacturing|manufacture|"
        r"manufactured|mfd|production|produced)"
    )

    if re.search(numeric_pattern, normalized):
        return True

    # --------------------------------------------------
    # Word-number relative declaration
    #
    # Handles OCR output such as:
    #
    # SIXMONTHSFROMTHEDATEOFPA
    # --------------------------------------------------

    word_numbers = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "sixty",
        "ninety",
    ]

    number_pattern = "|".join(word_numbers)

    word_relative_pattern = (
        rf"(?:{number_pattern})"
        r"(?:day|days|month|months|year|years)"
        r"from"
        r"(?:the)?"
        r"(?:dateof)?"
        r"(?:packing|packed|manufacturing|manufacture|"
        r"manufactured|mfd|production|produced)"
    )

    if re.search(word_relative_pattern, normalized):
        return True

    # --------------------------------------------------
    # Truncated OCR variant
    #
    # Example:
    # SIXMONTHSFROMTHEDATEOFPA
    #
    # "PA" is likely the beginning of "PACKING".
    # We accept this only when the rest of the structure
    # strongly indicates a relative best-before declaration.
    # --------------------------------------------------

    truncated_pattern = (
        rf"(?:{number_pattern})"
        r"(?:day|days|month|months|year|years)"
        r"from"
        r"(?:the)?"
        r"dateof"
        r"(?:p|pa|pac|pack|packi|packin)"
    )

    if re.search(truncated_pattern, normalized):
        return True

    return False


def _parse_date(date_value):
    """
    Converts supported OCR/AI date formats into datetime.

    Supports both complete dates and month/year formats.
    """

    if not date_value:
        return None

    date_text = str(date_value).strip()

    formats = [
        # Complete dates - four digit year
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%d.%m.%Y",

        # Complete dates - two digit year
        "%d-%m-%y",
        "%d/%m/%y",

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