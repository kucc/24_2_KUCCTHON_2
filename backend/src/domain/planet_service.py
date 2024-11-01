from fastapi import HTTPException, status
from models import Item, Planet
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
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
