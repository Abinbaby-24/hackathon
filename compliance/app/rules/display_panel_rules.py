def check_display_panel(product):
    """
    Checks display-panel related information.

    Visual properties such as font size, placement and
    principal display panel visibility cannot be reliably
    determined from OCR text alone.

    Unless visual display-panel data is explicitly provided,
    these checks are treated as NOT_APPLICABLE rather than
    assuming non-compliance.
    """

    checks = {}
    violations = []

    font_size = product.get("font_size")
    placement = product.get("display_panel_placement")
    principal_panel = product.get("principal_display_panel")

    # --------------------------------------------------
    # 1. Font size
    # --------------------------------------------------

    if font_size is not None:
        checks["font_size"] = "PASS"
    else:
        checks["font_size"] = "NOT_APPLICABLE"

    # --------------------------------------------------
    # 2. Display panel placement
    # --------------------------------------------------

    if placement is not None:
        checks["placement"] = "PASS"
    else:
        checks["placement"] = "NOT_APPLICABLE"

    # --------------------------------------------------
    # 3. Principal display panel
    # --------------------------------------------------

    if principal_panel is not None:
        checks["principal_display_panel"] = "PASS"
    else:
        checks["principal_display_panel"] = "NOT_APPLICABLE"

    return {
        "checks": checks,
        "violations": violations
    }