from datetime import datetime as _datetime

from pydantic import BaseModel, Field


class LikeItem(BaseModel):
    id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    planet_id: int = Field(gt=0)
    liked_at: _datetime
