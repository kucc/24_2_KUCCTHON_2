from pydantic import BaseModel, Field


class PlanetItem(BaseModel):
    id: int=Field(title="id")
    user_id: int=Field(title="user_id")
    planet_name: str=Field(title="planet_name", description="행성 이름")
    head: int=Field(0, title="head", description="머리 아이템", ge=0)
    pet: int=Field(0, title="head", description="애완 아이템", ge=0)
    eye: int=Field(0, title="head", description="눈 아이템", ge=0)
    tool: int=Field(0, title="head", description="도구 아이템", ge=0)
    like_count: int=Field(title="like_count", description="좋아요 개수")


class ResGetPlanet(BaseModel):
  planet_name: str=Field(title="planet_name", description="행성 이름")
  user_id: int
  user_name: str=Field(title="user_name", description="행성 주인 닉네임")
  head: int=Field(0, title="head", description="머리 아이템", ge=0)
  pet: int=Field(0, title="head", description="애완 아이템", ge=0)
  eye: int=Field(0, title="head", description="눈 아이템", ge=0)
  tool: int=Field(0, title="head", description="도구 아이템", ge=0)
  like_count: int=Field(title="like_count", description="좋아요 개수")

class ResGetAllPlanet(BaseModel):
  data: list[ResGetPlanet]=Field(title="planet_list", description="행성 목록")
  count: int=Field(0, title="planet_count", description="전체 행성 개수", ge=0)


class ReqPutPlanetItem(BaseModel):
    id: int = Field(title="item_id", description="아이템 고유 id", gt=0)
