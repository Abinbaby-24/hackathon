from fastapi import APIRouter, HTTPException
from app.database.queries import (
    create_report,
    get_report
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.post("/")
def create_new_report(report: dict):
    result = create_report(report)

    if not result:
        raise HTTPException(
            status_code=500,
            detail="Failed to create report"
        )

    return result


@router.get("/{report_id}")
def get_single_report(report_id: str):
    result = get_report(report_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return result