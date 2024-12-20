import domain.auth_service as auth_service
import schema.auth_schema as auth_schemas
from config import Settings
from dependencies import get_current_user, get_db
from domain.auth_service import service_put_initial_planet
from fastapi import APIRouter, Depends, status
from schema.planet_schema import PlanetItem
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

settings = Settings()

# 신규 사용자 등록


@router.post(
    "/register",
    response_model=auth_schemas.RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="신규 사용자 등록 및 행성 생성",
    description="""신규 사용자 등록 및 행성 생성
    """,
    response_description={
        status.HTTP_201_CREATED: {"description": "User created"}
    }
)
async def register(
    request: auth_schemas.RegisterRequest,
    db: Session = Depends(get_db)
):
    return await auth_service.register(request, db)


@router.post(
    "/login",
    response_model=auth_schemas.LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="로그인",
    response_description={
        status.HTTP_200_OK: {"description": "Login successful"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
        status.HTTP_403_FORBIDDEN: {"description": "Invalid password"},
    }
)
async def login(
    request: auth_schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    if settings.ENVIRONMENT == "development":
        return await auth_service.login(request, db)
    # elif settings.ENVIRONMENT == "production":
    #     return await auth_service.login(request, db)


@router.put(
    "/initial-setting",
    response_model=PlanetItem,
    status_code=status.HTTP_200_OK,
    summary="행성 초기 설정"
)
def put_initial_planet(
    request: auth_schemas.PlanetSetting,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    response = service_put_initial_planet(request, current_user.id, db)
    return response
