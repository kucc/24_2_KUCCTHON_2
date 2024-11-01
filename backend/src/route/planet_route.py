from dependencies import get_current_user, get_db
from domain.planet_service import service_abandon_item, service_apply_item
from fastapi import APIRouter, Depends, status
from schema.planet_schema import PlanetItem, ReqPutPlanetItem
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/planet",
    tags=["planet"]
)

@router.put(
    "/random_item",
    summary="아이템 적용",
    response_model=PlanetItem,
    status_code=status.HTTP_200_OK
)
def put_item(
    item: ReqPutPlanetItem,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = service_apply_item(item.id, current_user.id, db)

    return result


@router.put(
    "/abandon_item/{item_type}",
    summary="아이템 버리기",
    response_model=PlanetItem,
    status_code=status.HTTP_200_OK
)
def abandon_item(
    item_type: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = service_abandon_item(item_type, current_user.id, db)

    return result
