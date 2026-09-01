import json
from unittest import result
from app.engine.validator import validate_product


def test_real_ai_product():

    product = {
        "manufacturer_packer_importer":
            "RAZY BAKERY UDYOG Plot No-G-3A, Sector-15 GIDA, Gorakhpur - 273209",

        "common_or_generic_name":
            "POTATO CHIPS",

        "is_imported":
            None,

        "country_of_origin":
            None,

        "net_quantity":
            "11+2=13g",

        "consumer_care_details":
            "Consumer Care Center address given above or call at "
            "Customer Care: +91-983875522, "
            "email: support@crazybakery.in, "
            "www.crazybakery.in",

        "unit_sale_price":
            None,

        "selling_price":
            None,

        "mrp":
            "5/-",

        "mrp_inclusive_of_taxes":
            True,

        "manufacturing_date":
            "14-08-22",

        "packing_date":
            None,

        "import_date":
            None,

        "best_before":
            "SIXMONTHSFROMTHEDATEOFPA",

        "use_by":
            "09-02-23",

        "package_type":
            None
    }

    result = validate_product(product)

    print("\nCOMPLIANCE RESULT:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    assert result is not None
    assert "status" in result
    assert "score" in result
    assert "checks" in result
    assert "violations" in result