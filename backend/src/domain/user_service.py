from fastapi import HTTPException, status
from models import User, Planet
from schema.user_schema import ResGetUser
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session


def service_get_user_ticket(user_id, db: Session):
    stmt = select(Planet).where(Planet.user_id == user_id)

    try:
        ticket = db.execute(stmt).scalar_one()

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

    return ticket

def service_reduce_user_ticket(user_id, count, db: Session):
    stmt = select(Planet).where(Planet.user_id == user_id)

    try:
        planet = db.execute(stmt).scalar_one()

        if not planet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No user"
            )
        if(planet.ticket < count):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No enough tickets",
        )

        planet.like_count = planet.like_count - count

        db.flush()

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Integrity Error occurred during update the Review item.: {str(e)}",
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

    response = ResGetUser(
        id = planet.id,
        user_name = planet.user_name,
        ticket = planet.like_count,
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
