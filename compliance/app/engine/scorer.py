def calculate_score(checks):
    """
    Calculates a project-level compliance score from
    validation checks.

    PASS            = full marks
    REVIEW          = partial marks
    FAIL            = zero marks
    NOT_APPLICABLE  = excluded from scoring

    NOTE:
    The percentage score is a system-generated inspection
    indicator. It is not a percentage defined by the
    Legal Metrology rules.
    """

    total = 0
    passed = 0
    review = 0
    failed = 0
    not_applicable = 0

    def process_check(value):
        nonlocal total
        nonlocal passed
        nonlocal review
        nonlocal failed
        nonlocal not_applicable

        # Handle nested dictionaries
        if isinstance(value, dict):

            for nested_value in value.values():
                process_check(nested_value)

            return

        # Ignore values that are not validation statuses
        if value not in [
            "PASS",
            "FAIL",
            "REVIEW",
            "NOT_APPLICABLE"
        ]:
            return

        # NOT_APPLICABLE should not affect the score
        if value == "NOT_APPLICABLE":

            not_applicable += 1
            return

        # Count only applicable checks
        total += 1

        if value == "PASS":

            passed += 1

        elif value == "REVIEW":

            review += 1

        elif value == "FAIL":

            failed += 1

    # Process all checks
    process_check(checks)

    # No applicable checks
    if total == 0:

        return {
            "score": 0,
            "total_checks": 0,
            "passed": 0,
            "review": 0,
            "failed": 0,
            "not_applicable": not_applicable
        }

    # --------------------------------------------------
    # Score calculation
    # --------------------------------------------------
    #
    # PASS   = 100%
    # REVIEW = 50%
    # FAIL   = 0%
    #
    # NOT_APPLICABLE is excluded.
    #

    score = (
        (passed + (review * 0.5))
        / total
    ) * 100

    return {
        "score": round(score, 2),
        "total_checks": total,
        "passed": passed,
        "review": review,
        "failed": failed,
        "not_applicable": not_applicable
    }