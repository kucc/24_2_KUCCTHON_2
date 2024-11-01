from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Comment(BaseModel):
  user_name: str=Field(title="user_name", description="방명록 글쓴이 닉네임")
  content: str=Field(title="content", description="방명록 내용")
  created_at: datetime

class ResGetComments(BaseModel):
  planet_name: str=Field(title="planet_name", description="행성 이름")
  user_name: str=Field(title="user_name", description="행성 주인 닉네임")
  comments: List[Comment]=Field(title="user_name", description="행성 주인 닉네임")
  count: int=Field(title="count", description="방명록 개수")

class RouteReqPostComments(BaseModel):
  current_user_id: int
  content: str
class ReqPostComments(BaseModel):
  user_id: int=Field(title="user_id", description="방명록 글쓴이 id")
  planet_user_id: int=Field(title="planet_user_id", description="행성 주인 id")
  content: str

class ResPostComments(BaseModel):
  user_id: int=Field(title="user_id", description="방명록 글쓴이 id")
  planet_user_id: int=Field(title="planet_user_id", description="행성 주인 id")
  content: str
