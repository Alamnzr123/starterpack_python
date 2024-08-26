import uvicorn
from models import Books as ModelUser
from schema import Books as SchemaUser
from fastapi import HTTPException
from typing import List
from app import app

@app.post("/books/")
async def create_books(user: SchemaUser):
    books_id = await ModelUser.create(**user.model_dump())
    return {"books_id": books_id}

@app.put("/books/{id}")
async def update_books(id: int, user: SchemaUser):
    books_id = await ModelUser.update_books(id, **user.model_dump(exclude_unset=True))
    return {"books_id": books_id}

@app.get("/books/", response_model=List[SchemaUser])
async def get_user_All():
    book = await ModelUser.get_all()
    return book


@app.get("/books/{id}", response_model=SchemaUser)
async def get_user_byId(id: int):
    book = await ModelUser.get_byId(id)
    return SchemaUser(**book).dict()

@app.delete("/books/{id}")
async def delete_books(id: int):
     await ModelUser.delete_books(id)
     return {"message": "Data Delete"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)