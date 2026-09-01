from typing import Optional

from pydantic import BaseModel


class ProductData(BaseModel):
    product_name: Optional[str] = None
    manufacturer: Optional[str] = None
    mrp: Optional[str] = None
    net_quantity: Optional[str] = None
    packing_date: Optional[str] = None
    consumer_care: Optional[str] = None
    country_of_origin: Optional[str] = None
    best_before: Optional[str] = None