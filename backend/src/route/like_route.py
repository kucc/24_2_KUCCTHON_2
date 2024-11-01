from dependencies import get_current_user, get_db
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
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = service_create_like(current_user.id, planet_id, db)
    return result
