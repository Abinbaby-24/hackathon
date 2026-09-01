from app.engine.validator import validate_product


def test_compliant_product():
    product = {
        "manufacturer_packer_importer": "ABC Foods Pvt Ltd",
        "is_imported": False,
        "common_or_generic_name": "Rice",
        "net_quantity": "1 kg",
        "mrp": 120,
        "selling_price": 110,
        "mrp_inclusive_of_taxes": True,
        "consumer_care_details": "1800-123-456",
        "unit_sale_price": "₹120/kg",
        "manufacturing_date": "2026-05",
        "best_before": "2027-05"
    }

    result = validate_product(product)

    assert result["status"] == "COMPLIANT"


def test_missing_mandatory_information():
    product = {
        "manufacturer_packer_importer": "",
        "is_imported": False,
        "common_or_generic_name": "",
        "net_quantity": "",
        "mrp": None,
        "consumer_care_details": "",
        "unit_sale_price": "",
        "manufacturing_date": "2026-05",
        "best_before": "2027-05"
    }

    result = validate_product(product)

    assert result["status"] == "NON_COMPLIANT"
    assert result["statistics"]["failed"] > 0


def test_selling_price_above_mrp():
    product = {
        "manufacturer_packer_importer": "ABC Foods Pvt Ltd",
        "is_imported": False,
        "common_or_generic_name": "Rice",
        "net_quantity": "1 kg",
        "mrp": 120,
        "selling_price": 150,
        "mrp_inclusive_of_taxes": True,
        "consumer_care_details": "1800-123-456",
        "unit_sale_price": "₹120/kg",
        "manufacturing_date": "2026-05",
        "best_before": "2027-05"
    }

    result = validate_product(product)

    assert result["status"] == "NON_COMPLIANT"


def test_invalid_quantity():
    product = {
        "manufacturer_packer_importer": "ABC Foods Pvt Ltd",
        "is_imported": False,
        "common_or_generic_name": "Rice",
        "net_quantity": "ABC",
        "mrp": 120,
        "selling_price": 110,
        "mrp_inclusive_of_taxes": True,
        "consumer_care_details": "1800-123-456",
        "unit_sale_price": "₹120/kg",
        "manufacturing_date": "2026-05",
        "best_before": "2027-05"
    }

    result = validate_product(product)

    assert result["status"] == "NON_COMPLIANT"


def test_invalid_date_order():
    product = {
        "manufacturer_packer_importer": "ABC Foods Pvt Ltd",
        "is_imported": False,
        "common_or_generic_name": "Rice",
        "net_quantity": "1 kg",
        "mrp": 120,
        "selling_price": 110,
        "mrp_inclusive_of_taxes": True,
        "consumer_care_details": "1800-123-456",
        "unit_sale_price": "₹120/kg",
        "manufacturing_date": "2027-05",
        "best_before": "2026-05"
    }

    result = validate_product(product)

    assert result["status"] == "NON_COMPLIANT"


def test_imported_product_without_country_of_origin():
    product = {
        "manufacturer_packer_importer": "ABC Imports",
        "is_imported": True,
        "country_of_origin": "",
        "common_or_generic_name": "Chocolate",
        "net_quantity": "100 g",
        "mrp": 150,
        "selling_price": 150,
        "mrp_inclusive_of_taxes": True,
        "consumer_care_details": "1800-123-456",
        "unit_sale_price": "₹150/kg",
        "manufacturing_date": "2026-05",
        "best_before": "2027-05"
    }

    result = validate_product(product)

    assert result["status"] == "NON_COMPLIANT"


def test_insufficient_information_returns_review():
    product = {
        "manufacturer_packer_importer": "ABC Foods Pvt Ltd",
        "is_imported": False,
        "common_or_generic_name": "Rice",
        "net_quantity": "1 kg",
        "mrp": 120,
        "selling_price": 110,
        "mrp_inclusive_of_taxes": None,
        "consumer_care_details": "1800-123-456",
        "unit_sale_price": "₹120/kg",
        "manufacturing_date": None,
        "best_before": None
    }

    result = validate_product(product)

    assert result["status"] == "REVIEW"