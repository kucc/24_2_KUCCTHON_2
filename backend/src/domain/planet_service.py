from datetime import datetime

from fastapi import HTTPException, status
from models import Comments, Item, Planet, User
from schema.comments_schema import Comment, ReqPostComments, ResGetComments, ResPostComments
from schema.planet_schema import ResGetPlanet
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session


def service_apply_item(item_id, user_id, db: Session):
    planet_stmt = select(Planet).where(
        Planet.user_id == user_id
    )
    item_stmt = select(Item).where(
        Item.id == item_id
    )
    try:
        planet = db.execute(planet_stmt).scalar_one_or_none()
        item = db.execute(item_stmt).scalar_one_or_none()

        if not planet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Planet not found"
            )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )

        # Use a dictionary to map item places to planet attributes
        item_place_to_attr = {
            "head": "head",
            "pet": "pet",
            "eye": "eye",
            "tool": "tool"
        }

        if item.place in item_place_to_attr:
            setattr(planet, item_place_to_attr[item.place], item.id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid item place"
            )

        db.flush()

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Integrity Error occurred during update: {str(e)}",
        ) from e

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during update: {str(e)}",
        ) from e

    else:
        db.commit()
        db.refresh(planet)

    return planet


def service_abandon_item(item_type, user_id, db: Session):
    stmt = select(Planet).where(
        Planet.user_id == user_id
    )

    try:
        planet = db.execute(stmt).scalar_one_or_none()

        if not planet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Planet not found"
            )

        item_place_to_attr = {
            "head": "head",
            "pet": "pet",
            "eye": "eye",
            "tool": "tool"
        }

        if item_type in item_place_to_attr:
            setattr(planet, item_place_to_attr[item_type], 0)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid item place"
            )
        db.flush()

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Integrity Error occurred during update: {str(e)}",
        ) from e

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during update: {str(e)}",
        ) from e

    else:
        db.commit()
        db.refresh(planet)

    return planet


async def service_read_all_planet(db: Session) -> list[ResGetPlanet]:
    planets = db.execute(select(Planet).order_by(Planet.id)).scalars().all()  # 모든 행 가져오기
    response = []

    for planet in planets:
        # User 조회
        stmt = select(User).where(User.id == planet.user_id)
        try:
            user = db.execute(stmt).scalar_one()  # 단일 사용자 가져오기
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User not found for planet {planet.planet_name}") from NoResultFound

        # 응답 구성
        response.append(
            ResGetPlanet(
                planet_name=planet.planet_name,
                user_id=user.id,
                user_name=user.user_name,
                head=planet.head,
                pet=planet.pet,
                eye=planet.eye,
                tool=planet.tool,
                like_count=planet.like_count,
            )
        )

    return response

async def service_read_planet(user_id: int, db: Session):
    stmt = select(Planet).where(Planet.user_id==user_id)
    try:
        planet = db.execute(stmt).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found") from NoResultFound
    stmt = select(User).where(User.id == planet.user_id)
    try:
        user = db.execute(stmt).scalar_one()  # 단일 사용자 가져오기
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found for planet {planet.planet_name}") from NoResultFound

    response = ResGetPlanet(
        planet_name=planet.planet_name,
        user_id=user.id,
        user_name=user.user_name,
        head=planet.head,
        pet=planet.pet,
        eye=planet.eye,
        tool=planet.tool,
        like_count=planet.like_count
    )

    return response

async def service_create_comments(request: ReqPostComments, db: Session):
    planet = db.execute(select(Planet).where(Planet.user_id==request.planet_user_id)).scalar_one()
    comment_request = Comments(
        user_id=request.user_id,
        planet_id=planet.id,
        content=request.content,
        created_at=datetime.now()
    )

    try:
        db.add(comment_request)
        db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred: {str(e)}") from e
    else:
        db.commit()
        db.refresh(comment_request)

        result = ResPostComments(
            user_id=request.user_id,
            planet_user_id=planet.id,
            content=request.content,
        )
    return result

async def service_read_comments(user_id: int, db: Session):
    stmt = select(Planet).where(Planet.user_id==user_id)
    try:
        planet = db.execute(stmt).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found") from NoResultFound
    stmt = select(Comments).where(Comments.planet_id == planet.id).order_by(Comments.created_at)
    try:
        my_comments = db.execute(stmt).scalars().all()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comments not found for planet {planet.planet_name}") from NoResultFound
    comments = []
    for my_comment in my_comments:
        # User 조회
        stmt = select(User).where(User.id == my_comment.user_id)
        try:
            user = db.execute(stmt).scalar_one()  # 단일 사용자 가져오기
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found for comment") from NoResultFound

    # 응답 구성
    comments.append(
        Comment(
            user_name=user.user_name,
            content=my_comment.content,
            created_at=my_comment.created_at,
        )
    )
  response = ResGetComments(
    planet_name=planet.planet_name,
    user_name=user.user_name,
    comments=comments,
    count=len(comments),
  )
  return response

def service_increase_like(planet_id: int, count: int, db: Session) -> None:
    stmt = select(Planet).where(Planet.user_id == planet_id)
    try:
        planet = db.execute(stmt).scalar_one_or_none()
        if not planet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Planet not found",
            )

        planet.like_count += count
        db.flush()

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Integrity Error occurred during update: {str(e)}",
        ) from e

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during update: {str(e)}",
        ) from e

    else:
        db.commit()
        db.refresh(planet)
