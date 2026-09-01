def check_mandatory_declarations(product):
    """
    Checks the mandatory declarations required on packaged commodities.

    The function checks:
    - Manufacturer / packer / importer details
    - Country of origin for imported products
    - Common / generic name
    - Net quantity
    - MRP
    - Consumer care details
    - Unit sale price where applicable
    """

    checks = {}
    violations = []

    # --------------------------------------------------
    # 1. Manufacturer / Packer / Importer
    # --------------------------------------------------

    manufacturer_details = product.get("manufacturer_packer_importer")

    if manufacturer_details:
        checks["manufacturer_packer_importer"] = "PASS"
    else:
        checks["manufacturer_packer_importer"] = "FAIL"

        violations.append({
            "field": "manufacturer_packer_importer",
            "message": (
                "Manufacturer, packer or importer name and address "
                "details are missing."
            )
        })

    # --------------------------------------------------
    # 2. Country of Origin
    # --------------------------------------------------

    is_imported = product.get("is_imported")

    if is_imported is True:

        if product.get("country_of_origin"):
            checks["country_of_origin"] = "PASS"

        else:
            checks["country_of_origin"] = "FAIL"

            violations.append({
                "field": "country_of_origin",
                "message": (
                    "Country of origin is missing for an imported product."
                )
            })

    elif is_imported is False:

        checks["country_of_origin"] = "NOT_APPLICABLE"

    else:

        checks["country_of_origin"] = "REVIEW"

        violations.append({
            "field": "country_of_origin",
            "message": (
                "Could not determine whether the product is imported."
            )
        })

    # --------------------------------------------------
    # 3. Common / Generic Name
    # --------------------------------------------------

    if product.get("common_or_generic_name"):

        checks["common_or_generic_name"] = "PASS"

    else:

        checks["common_or_generic_name"] = "FAIL"

        violations.append({
            "field": "common_or_generic_name",
            "message": (
                "Common or generic name of the commodity is missing."
            )
        })

    # --------------------------------------------------
    # 4. Net Quantity
    # --------------------------------------------------

    if product.get("net_quantity"):

        checks["net_quantity"] = "PASS"

    else:

        checks["net_quantity"] = "FAIL"

        violations.append({
            "field": "net_quantity",
            "message": "Net quantity declaration is missing."
        })

    # --------------------------------------------------
    # 5. MRP
    # --------------------------------------------------

    if product.get("mrp") is not None:

        checks["mrp"] = "PASS"

    else:

        checks["mrp"] = "FAIL"

        violations.append({
            "field": "mrp",
            "message": (
                "Maximum Retail Price (MRP) is missing."
            )
        })

    # --------------------------------------------------
    # 6. Consumer Care Details
    # --------------------------------------------------

    if product.get("consumer_care_details"):

        checks["consumer_care_details"] = "PASS"

    else:

        checks["consumer_care_details"] = "FAIL"

        violations.append({
            "field": "consumer_care_details",
            "message": (
                "Consumer care details are missing."
            )
        })

    # --------------------------------------------------
    # 7. Unit Sale Price
    # --------------------------------------------------

    package_type = product.get("package_type")

    # Unit sale price may not apply to certain package types.
    if package_type in [
        "combination",
        "group",
        "multi_piece"
    ]:

        checks["unit_sale_price"] = "NOT_APPLICABLE"

    elif product.get("unit_sale_price"):

        checks["unit_sale_price"] = "PASS"

    else:

        checks["unit_sale_price"] = "REVIEW"

        violations.append({
            "field": "unit_sale_price",
            "message": (
                "Unit sale price could not be verified. "
                "Applicability depends on the package type."
            )
        })

    return {
        "checks": checks,
        "violations": violations
    }