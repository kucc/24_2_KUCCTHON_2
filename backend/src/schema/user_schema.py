from pydantic import BaseModel, Field


class ResGetUser(BaseModel):
    id: int = Field(title="item_id", description="아이템 고유 id", gt=0)
    user_name: str = Field(title="user_name", description="사용자 이름")
    ticket: int = Field(title="ticket", description="뽑기용 티켓")

