import jwt
from config import Settings
from database import get_db_session
from fastapi import Depends, Header, HTTPException, status
from models import User
from sqlalchemy.orm import Session


def get_db():
    try:
        session = get_db_session()
        yield session
    finally:
        session.close()

async def get_current_user(token=Header(None), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(token, key=Settings().JWT_SECRET_KEY, algorithms=Settings().JWT_ALGORITHM)
    user_id: int = int(payload.get("sub"))
    if user_id is None:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
