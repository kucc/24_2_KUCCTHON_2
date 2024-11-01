from fastapi import HTTPException, status
from models import Comments, Planet, User
from schema.comments_schema import Comment, ResGetComments
from schema.planet_schema import ResGetPlanet
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session


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

async def service_read_comments(user_id: int, db: Session):
  stmt = select(Planet).where(Planet.user_id==user_id)
  try:
    planet = db.execute(stmt).scalar_one()
  except NoResultFound:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail="Not found") from NoResultFound
  stmt = select(Comments).where(Comments.planet_id == planet.id)
  try:
    my_comments = db.execute(stmt).order_by(Comments.created_at).scalars().all()
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
