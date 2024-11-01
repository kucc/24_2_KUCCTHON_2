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
    head = Column(Integer, nullable=True)
