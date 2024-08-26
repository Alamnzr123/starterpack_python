from pydantic import BaseModel
from datetime import datetime

class Authors(BaseModel):
    name: str
    bio: str
    birth_date: str
    class Config:
        orm_mode = True