from typing import Optional

from pydantic import BaseModel


class ProductData(BaseModel):
    manufacturer_packer_importer: Optional[str] = None
    common_or_generic_name: Optional[str] = None

    is_imported: Optional[bool] = None
    country_of_origin: Optional[str] = None

    net_quantity: Optional[str] = None

    consumer_care_details: Optional[str] = None

    unit_sale_price: Optional[str] = None
    selling_price: Optional[str] = None

    mrp: Optional[str] = None
    mrp_inclusive_of_taxes: Optional[bool] = None

    manufacturing_date: Optional[str] = None
    packing_date: Optional[str] = None
    import_date: Optional[str] = None
    best_before: Optional[str] = None
    use_by: Optional[str] = None

    package_type: Optional[str] = None