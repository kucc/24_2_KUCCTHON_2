from dependencies import get_db
from domain.item_service import service_draw_random_item
from domain.user_service import service_get_user_ticket, service_reduce_user_ticket
from fastapi import APIRouter, Depends, HTTPException, status
from schema.item_schema import ResGetItem
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/item",
    tags=["item"]
)

@router.get(
    "/random_item",
    summary="랜덤 아이템 뽑기",
    response_model=ResGetItem,
    status_code=status.HTTP_200_OK
)
def get_random_item(
    user_id: int,
    db: Session = Depends(get_db),
):
    if (service_get_user_ticket(user_id, db) > 0):
        service_reduce_user_ticket(user_id, 1, db)
        result = service_draw_random_item(db)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No enough tickets",
        )

    return result
