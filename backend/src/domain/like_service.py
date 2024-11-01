
from datetime import datetime as _datetime
from datetime import timedelta

from domain.planet_service import service_increase_like
from domain.user_service import service_increase_ticket
from fastapi import HTTPException, status
from models import Likes, Planet
from sqlalchemy import select
from sqlalchemy.orm import Session


def service_create_like(user_id, planet_id, db: Session):
    planet_stmt = select(Planet).where(Planet.id == planet_id)
    # Likes에 좋아요 정보를 저장.
    # 1분이 지났는지 아닌지 파악.
    # 좋아요를 누르면 User의 ticket, Planet의 like_count가 1씩 증가하게. 이거 따로 빼기

    try:
        can_like = can_user_like(user_id, db)
        if not can_like:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="You can only like once per one minute. Please try again later."
            )
        planet = db.execute(planet_stmt).scalar_one_or_none()
        if not planet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Planet not found."
            )

        try:
            service_increase_like(planet_id, 1, db)
            service_increase_ticket(planet.user_id, 1, db) # 행성의 사용자에게 (= 좋아요를 받는 사용자에게)

            new_like = Likes(
                user_id=user_id,
                planet_id=planet_id,
                liked_at=_datetime.now()
            )
            db.add(new_like)
            db.flush()
            db.commit()
            db.refresh(new_like)

            return new_like
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error occurred: {str(e)}"
            ) from e

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An error occurred: {str(e)}"
        ) from e

def can_user_like(user_id: int, db: Session) -> bool:
    try:
        one_minute_ago = _datetime.now() - timedelta(minutes=1)

        stmt = (
            select(Likes)
            .where(Likes.user_id == user_id)
            .order_by(Likes.liked_at.desc())
            .limit(1)
        )

        last_like = db.execute(stmt).scalar_one_or_none()

        if last_like:
            if last_like.liked_at > one_minute_ago:
                return False # Not enough time has passed
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking like timing: {str(e)}"
        ) from e
