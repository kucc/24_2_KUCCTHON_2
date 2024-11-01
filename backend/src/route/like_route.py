from dependencies import get_db
from domain.like_service import service_create_like
from fastapi import APIRouter, Depends, status
from schema.like_schema import LikeItem
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/like",
    tags=["like"]
)

@router.put(
    "/{planet_id}",
    summary="좋아요 누르기",
    response_model=LikeItem,
    status_code=status.HTTP_200_OK
)
async def create_like(
    planet_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    result = service_create_like(user_id, planet_id, db)
    return result
