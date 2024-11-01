from database import get_db_session


def get_db():
    try:
        session = get_db_session()
        yield session
    finally:
        session.close()
