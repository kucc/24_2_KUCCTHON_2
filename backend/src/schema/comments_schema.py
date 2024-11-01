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
