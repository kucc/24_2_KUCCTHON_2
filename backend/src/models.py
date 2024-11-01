from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    login_id = Column(String(20), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    user_name = Column(String(20), nullable=False)

    planet = relationship("Planet", back_populates="user")
    comments = relationship("Comments", back_populates="user")
    likes = relationship("Likes", back_populates="user")

class Planet(Base):
    __tablename__ = "planet"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    planet_name = Column(String(20), nullable=False)
    head = Column(Integer, nullable=False)
    pet = Column(Integer, nullable=False)
    eye = Column(Integer, nullable=False)
    tool = Column(Integer, nullable=False)
    like_count = Column(Integer, default=0)
    
    user = relationship("User", back_populates="planet")
    comments = relationship("Comments", back_populates="planet")
    likes = relationship("Likes", back_populates="planet")

class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    planet_id = Column(Integer, ForeignKey("planet.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.current_timestamp())

    user = relationship("User", back_populates="comments")
    planet = relationship("Planet", back_populates="comments")


class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    planet_id = Column(Integer, ForeignKey("planet.id"), nullable=False)
    liked_at = Column(TIMESTAMP, nullable=False, default=func.current_timestamp())

    user = relationship("User", back_populates="likes")
    planet = relationship("Planet", back_populates="likes")