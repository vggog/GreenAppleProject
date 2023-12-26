from starlette import status
from fastapi import APIRouter, Depends, HTTPException

from src.master.service import Servise
from src.customer.schemas import RepairOrderSchema


router = APIRouter()


@router.get(
    "/track/{track_number}",
    response_model=RepairOrderSchema,
)
def hello_world_view(
        track_number: int,
        service: Servise = Depends(Servise),
):
    repair_order = service.get_repair_order(track_number)

    if repair_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return repair_order
