import random

from fastapi import HTTPException, status
from models import Item
from sqlalchemy import select
from sqlalchemy.orm import Session


def service_draw_random_item(db: Session):
    random_id = random.randint(1, 6) # 현재 20번까지 Item이 존재.

    stmt1 = select(Item).where(Item.id == random_id)

    try:
        random_item = db.execute(stmt1).scalar_one()

        if not random_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No items available"
            )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during update: {str(e)}",
        ) from e

    return random_item
