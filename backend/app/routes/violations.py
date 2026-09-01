from fastapi import APIRouter, HTTPException
from app.database.queries import (
    create_violation,
    get_violations
)

router = APIRouter(
    prefix="/violations",
    tags=["Violations"]
)


@router.get("/{inspection_id}")
def get_inspection_violations(inspection_id: str):
    return get_violations(inspection_id)


@router.post("/")
def create_new_violation(violation: dict):
    result = create_violation(violation)

    if not result:
        raise HTTPException(
            status_code=500,
            detail="Failed to create violation"
        )

    return result