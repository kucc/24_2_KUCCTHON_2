from config import Settings
from dependencies import get_db
from domain.planet_service import service_read_all_planet, service_read_comments, service_read_planet, service_create_comments
from fastapi import APIRouter, Depends, status
from schema.comments_schema import ReqPostComments, ResGetComments, ResPostComments, RouteReqPostComments
from schema.planet_schema import ResGetAllPlanet, ResGetPlanet
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

@router.post(
    "/{user_id}/comments",
    summary="행성 방명록 작성",
    response_model=ResPostComments,
    status_code=status.HTTP_200_OK,
)
async def get_comments(
    user_id: int,
    request: RouteReqPostComments,
    db: Session = Depends(get_db)
):
    domain_req=ReqPostComments(
      user_id=request.current_user_id,
      planet_user_id=user_id,
      content=request.content,
    )
    result = await service_create_comments(domain_req, db)
    return result

@router.get(
    "/{user_id}/comments",
    summary="행성 방명록 조회",
    response_model=ResGetComments,
    status_code=status.HTTP_200_OK,
)
async def get_comments(
    user_id: int,
    db: Session = Depends(get_db)
):
    result = await service_read_comments(user_id, db)
    return result
