from domain.token_service import create_user_tokens
from fastapi import HTTPException, status
from models import Planet, User
from schema.auth_schema import LoginRequest, LoginResponse, RegisterRequest, UserInfo
from sqlalchemy.orm import Session


async def register(request: RegisterRequest, db: Session):

    # Check if user information exists in the DB
    user = db.query(User).filter(User.login_id == request.login_id).first()

    # If user information does not exist in the DB, create a new user
    if user is None:
        user = User(
            login_id=request.login_id,
            password=request.password,
            user_name=request.user_name,
            ticket=0
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        planet = Planet(
            user_id=user.id,
            planet_name=request.planet_name,
            head=0,
            pet=0,
            eye=0,
            tool=0,
            like_count=0,
        )
        db.add(planet)
        db.commit()
        db.refresh(planet)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    # Create JWT tokens
    token_response = create_user_tokens(user.id)

    return {
        "token": token_response,
        "user": {
            "id": user.id,
            "user_name": user.user_name,
            "login_id": user.login_id,
            "password": user.password
        },
        "planet": planet.planet_name,
    }

async def login(
        request: LoginRequest,
        db: Session):
    # Authenticate user
    # Check if user information exists in the DB
    user = db.query(User).filter(User.login_id == request.login_id).first()

    # If user information does not exist in the DB, return error
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.password != request.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password is wrong")

    # Create JWT tokens
    token_response = create_user_tokens(user.id)

    # Prepare user response
    user_response = UserInfo(
        id=user.id,
        user_name=user.user_name,
        login_id=user.login_id,
        password=user.password
    )

    # Return login response
    return LoginResponse(
        token=token_response,
        user=user_response
    )
