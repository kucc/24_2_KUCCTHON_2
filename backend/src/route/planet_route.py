from config import Settings
from dependencies import get_current_user, get_db
from domain.planet_service import service_abandon_item, service_apply_item, service_read_all_planet, service_read_planet
from fastapi import APIRouter, Depends, status
from schema.planet_schema import PlanetItem, ReqPutPlanetItem, ResGetAllPlanet, ResGetPlanet
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/planet",
    tags=["planet"]
)

settings = Settings()

@router.get(
    "/",
    summary="모든 행성 목록 조회",
    response_model=ResGetAllPlanet,
    status_code=status.HTTP_200_OK,
)
async def get_all_planets(
    db: Session = Depends(get_db)
):
    domain_res = await service_read_all_planet(db)
    result = ResGetAllPlanet(data=domain_res, count=len(domain_res))
    return result

@router.get(
    "/{user_id}/",
    summary="행성 조회",
    response_model=ResGetPlanet,
    status_code=status.HTTP_200_OK,
)
async def get_planet(
    user_id: int,
    db: Session = Depends(get_db)
):
    result = await service_read_planet(user_id, db)

    return result

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
