from pydantic import BaseModel, Field


class ResGetItem(BaseModel):
    id: int = Field(title="item_id", description="아이템 고유 id", gt=0)
    place: str = Field(title="place", description="아이템 장착 위치")
    name: str = Field(title="name", description="아이템 이름")
