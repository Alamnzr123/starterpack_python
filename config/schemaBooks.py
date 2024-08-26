from pydantic import BaseModel
from datetime import datetime


class Books(BaseModel):
    title: str
    description: str = None
    publish_date: datetime
    author_id: str
    class Config:
        orm_mode = True