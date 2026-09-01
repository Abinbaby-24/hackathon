from fastapi import APIRouter
from pydantic import BaseModel
from app.database.supabase import supabase

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


class Product(BaseModel):
    product_name: str
    manufacturer: str
    mrp: str
    net_quantity: str
    packing_date: str
    consumer_care: str
    country_of_origin: str
    best_before: str


@router.get("/")
def get_products():
    response = supabase.table("products").select("*").execute()
    return response.data


@router.post("/")
def create_product(product: Product):
    response = (
        supabase
        .table("products")
        .insert(product.model_dump())
        .execute()
    )

    return response.data