from sqlalchemy import TIMESTAMP, Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text
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


class Planet(Base):
    __tablename__ = "planet"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    planet_name = Column(String(20), nullable=False)
    head = Column(Integer, nullable=True)
    pet = Column(Integer, nullable=True)
    eye = Column(Integer)
    tool = Column(Integer, nullable=True)
    like_count = Column(Integer, default=0)
    
    user = relationship("User", back_populates="planet")
    comments = relationship("Comments", back_populates="comments")


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    planet_id = Column(Integer, ForeignKey("planet.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.current_timestamp())

    planet = relationship("Planet", back_populates="comments")
    user = relationship("User", back_populates="planet")


class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)

