from fastapi import HTTPException, status
from models import User, Planet
from schema.user_schema import ResGetUser
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session


def service_get_user_ticket(user_id, db: Session):
    stmt = select(Planet).where(Planet.user_id == user_id)

    try:
        planet = db.execute(stmt).scalar_one()

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        ) from None

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return planet.like_count

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException, status

def service_reduce_user_ticket(user_id, count, db: Session):
    stmt = select(Planet).where(Planet.user_id == user_id)

    try:
        planet = db.execute(stmt).scalar_one_or_none()  # NoResultFound 예외를 피하기 위해 수정

        if planet is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No user found"
            )
        if planet.like_count < count:  # 티켓 수 확인
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough tickets",
            )

        planet.like_count -= count  # like_count 감소
        print(",,,,,?", planet.like_count)
        db.flush()  # 변경 사항을 데이터베이스에 반영

    except IntegrityError as e:
        db.rollback()  # 오류 발생 시 롤백
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Integrity Error occurred during update: {str(e)}",
        ) from e

    except Exception as e:
        db.rollback()  # 오류 발생 시 롤백
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"11Unexpected error occurred during update: {str(e)}",
        ) from e

    else:
        db.commit()  # 변경 사항 커밋
        db.refresh(planet)  # 업데이트된 planet 객체를 새로고침

    response = ResGetUser(
        id=planet.user_id,
        ticket=planet.like_count,  # like_count으로 업데이트
    )

    return response


def service_increase_ticket(user_id: int, count: int, db: Session) -> None:
    print(user_id)
    stmt = select(User).where(User.id == user_id)
    try:
        user = db.execute(stmt).scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user.ticket += count
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
        db.refresh(user)
