def determine_status(score_data, violations):
    """
    Determines the overall compliance status.

    Possible results:
        COMPLIANT
        NON_COMPLIANT
        REVIEW

    Rules:
        - Any confirmed FAIL means NON_COMPLIANT.
        - If there are no FAIL results but REVIEW exists,
          the result is REVIEW.
        - NOT_APPLICABLE checks do not affect the status.
        - If no applicable checks are available, return REVIEW.
    """

    failed_count = score_data.get("failed", 0)
    review_count = score_data.get("review", 0)
    total_checks = score_data.get("total_checks", 0)

    # --------------------------------------------------
    # 1. Confirmed failure
    # --------------------------------------------------

    if failed_count > 0:
        return "NON_COMPLIANT"

    # --------------------------------------------------
    # 2. No applicable checks
    # --------------------------------------------------

    if total_checks == 0:
        return "REVIEW"

    # --------------------------------------------------
    # 3. Human verification required
    # --------------------------------------------------

    if review_count > 0:
        return "REVIEW"

    # --------------------------------------------------
    # 4. All applicable checks passed
    # --------------------------------------------------

    return "COMPLIANT"