from fastapi import APIRouter
from pydantic import BaseModel
from app.database.supabase import supabase

router = APIRouter(
    prefix="/inspections",
    tags=["Inspections"]
)


class Inspection(BaseModel):
    product_id: str
    user_id: str
    image_url: str | None = None
    score: float | None = None
    status: str


@router.get("/")
def get_inspections():
    response = supabase.table("inspections").select("*").execute()
    return response.data


@router.post("/")
def create_inspection(inspection: Inspection):
    response = (
        supabase
        .table("inspections")
        .insert(inspection.model_dump())
        .execute()
    )

    return response.data