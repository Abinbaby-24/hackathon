def check_standard_pack(product):
    """
    Checks standard-pack-size related information.

    Standard pack-size verification requires commodity-specific
    information and applicable standard-pack data.

    When such information is unavailable, the check is treated
    as NOT_APPLICABLE rather than assuming non-compliance.
    """

    checks = {}
    violations = []

    standard_pack_size = product.get("standard_pack_size")
    commodity_name = product.get("common_or_generic_name")

    # --------------------------------------------------
    # 1. Commodity identification
    # --------------------------------------------------

    if commodity_name:
        checks["commodity_identified"] = "PASS"
    else:
        checks["commodity_identified"] = "NOT_APPLICABLE"

    # --------------------------------------------------
    # 2. Standard pack size
    # --------------------------------------------------

    if standard_pack_size is not None:
        checks["standard_pack_size"] = "PASS"
    else:
        checks["standard_pack_size"] = "NOT_APPLICABLE"

    return {
        "checks": checks,
        "violations": violations
    }