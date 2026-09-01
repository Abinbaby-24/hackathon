def check_display_panel(ocr_result, product=None):
    """
    Performs display-panel checks using OCR information.

    OCR can verify whether important declarations are present
    and where they appear on the package.

    Exact font-size and prominence requirements cannot be
    confirmed from OCR alone, so they are marked REVIEW only
    when the required CV measurement is unavailable.
    """

    checks = {}
    violations = []

    # --------------------------------------------------
    # 1. OCR availability
    # --------------------------------------------------

    if not isinstance(ocr_result, dict):

        checks["display_panel_ocr"] = "REVIEW"

        violations.append({
            "field": "display_panel",
            "message": (
                "OCR data is unavailable for "
                "display-panel verification."
            )
        })

        return {
            "checks": checks,
            "violations": violations
        }

    regions = ocr_result.get("regions", [])

    if not regions:

        checks["display_panel_ocr"] = "REVIEW"

        violations.append({
            "field": "display_panel",
            "message": "No OCR regions were detected."
        })

        return {
            "checks": checks,
            "violations": violations
        }

    # --------------------------------------------------
    # 2. OCR confidence
    # --------------------------------------------------

    valid_regions = [
        region for region in regions
        if isinstance(region, dict)
        and region.get("text")
    ]

    if not valid_regions:

        checks["display_panel_ocr"] = "REVIEW"

        violations.append({
            "field": "display_panel",
            "message": "OCR regions do not contain usable text."
        })

        return {
            "checks": checks,
            "violations": violations
        }

    checks["display_panel_ocr"] = "PASS"

    # --------------------------------------------------
    # 3. Combine detected text
    # --------------------------------------------------

    detected_text = " ".join(
        str(region.get("text", ""))
        for region in valid_regions
    ).lower()

    # --------------------------------------------------
    # Helper function
    # --------------------------------------------------

    def text_present(value):
        if not value:
            return False

        value = str(value).strip().lower()

        if not value:
            return False

        return value in detected_text

    # --------------------------------------------------
    # 4. Product name
    # --------------------------------------------------

    product_name = product.get("product_name") if product else None

    if product_name:

        if text_present(product_name):

            checks["product_name_visible"] = "PASS"

        else:

            checks["product_name_visible"] = "REVIEW"

            violations.append({
                "field": "product_name",
                "message": (
                    "Product name was extracted but could not "
                    "be located confidently in the OCR text."
                )
            })

    else:

        checks["product_name_visible"] = "NOT_APPLICABLE"

    # --------------------------------------------------
    # 5. Manufacturer
    # --------------------------------------------------

    manufacturer = product.get("manufacturer") if product else None

    if manufacturer:

        if text_present(manufacturer):

            checks["manufacturer_visible"] = "PASS"

        else:

            checks["manufacturer_visible"] = "REVIEW"

            violations.append({
                "field": "manufacturer",
                "message": (
                    "Manufacturer information was extracted "
                    "but could not be located confidently "
                    "in the OCR text."
                )
            })

    else:

        checks["manufacturer_visible"] = "NOT_APPLICABLE"

    # --------------------------------------------------
    # 6. MRP
    # --------------------------------------------------

    mrp = product.get("mrp") if product else None

    if mrp is not None:

        mrp_text = str(mrp).strip().lower()

        # OCR may contain ₹ while AI extraction may not.
        mrp_text_without_symbol = (
            mrp_text.replace("₹", "")
            .replace("rs.", "")
            .replace("rs", "")
            .strip()
        )

        if (
            mrp_text in detected_text
            or mrp_text_without_symbol in detected_text
        ):

            checks["mrp_visible"] = "PASS"

        else:

            checks["mrp_visible"] = "REVIEW"

            violations.append({
                "field": "mrp",
                "message": (
                    "MRP was extracted but could not be "
                    "located confidently in the OCR text."
                )
            })

    else:

        checks["mrp_visible"] = "REVIEW"

    # --------------------------------------------------
    # 7. Net quantity
    # --------------------------------------------------

    quantity = product.get("net_quantity") if product else None

    if quantity:

        quantity_text = str(quantity).strip().lower()

        if text_present(quantity_text):

            checks["quantity_visible"] = "PASS"

        else:

            checks["quantity_visible"] = "REVIEW"

            violations.append({
                "field": "net_quantity",
                "message": (
                    "Net quantity was extracted but could "
                    "not be located confidently in OCR text."
                )
            })

    else:

        checks["quantity_visible"] = "REVIEW"

    # --------------------------------------------------
    # 8. Bounding boxes
    # --------------------------------------------------

    boxes_available = all(
        isinstance(region.get("box"), list)
        and len(region.get("box")) == 4
        for region in valid_regions
    )

    if boxes_available:

        checks["text_position_data"] = "PASS"

    else:

        checks["text_position_data"] = "REVIEW"

        violations.append({
            "field": "display_panel",
            "message": (
                "OCR text position information is "
                "incomplete."
            )
        })

    # --------------------------------------------------
    # 9. Font/display measurement
    # --------------------------------------------------

    # OCR provides text and coordinates, but not reliable
    # physical font-size measurements.
    #
    # If a future CV module provides these measurements,
    # this section can perform the actual legal check.

    font_measurement = None

    if product:
        font_measurement = product.get("font_measurement")

    if font_measurement is None:

        checks["font_requirements"] = "NOT_APPLICABLE"

    elif font_measurement is True:

        checks["font_requirements"] = "PASS"

    elif font_measurement is False:

        checks["font_requirements"] = "FAIL"

        violations.append({
            "field": "font_requirements",
            "message": (
                "Display-panel text does not satisfy "
                "the configured font/display requirement."
            )
        })

    else:

        checks["font_requirements"] = "REVIEW"

    return {
        "checks": checks,
        "violations": violations
    }