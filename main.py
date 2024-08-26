import uvicorn
from models.books import Books as ModelBooks
from models.authors import Authors as ModelAuthors
from config.schemaBooks import Books as SchemaBooks
from config.schemaAuthors import Authors as SchemaAuthors
from typing import List
from app import app

# Books Routes
@app.post("/books/")
async def create_books(create_books: SchemaBooks):
    books_id = await ModelBooks.create(**create_books.model_dump())
    return {"books_id": books_id}

@app.put("/books/{id}")
async def update_books(id: int, create_books: SchemaBooks):
    books_id = await ModelBooks.update_books(id, **create_books.model_dump(exclude_unset=True))
    return {"books_id": books_id}

@app.get("/books/", response_model=List[SchemaBooks])
async def get_books_All():
    book = await ModelBooks.get_all()
    return book


@app.get("/books/{id}", response_model=SchemaBooks)
async def get_books_byId(id: int):
    book = await ModelBooks.get_byId(id)
    return SchemaBooks(**book).dict()

@app.delete("/books/{id}")
async def delete_books(id: int):
     await ModelBooks.delete_books(id)
     return {"message": "Data Delete"}


# Authors Routes

@app.post("/authors/")
async def create_authors(create_author: SchemaAuthors):
    books_id = await ModelAuthors.create(**create_author.model_dump())
    return {"author_id": books_id}

@app.put("/authors/{id}")
async def update_authors(id: int, create_author: SchemaAuthors):
    author = await ModelAuthors.update_authors(id, **create_author.model_dump(exclude_unset=True))
    return {"author_id": author}

@app.get("/authors/", response_model=List[SchemaAuthors])
async def get_authors_All():
    author = await ModelAuthors.get_all()
    return author


@app.get("/authors/{id}", response_model=SchemaAuthors)
async def get_authors_byId(id: int):
    author = await ModelAuthors.get_byId(id)
    return SchemaBooks(**author).dict()

@app.delete("/authors/{id}")
async def delete_authors(id: int):
     await ModelAuthors.delete_authors(id)
     return {"message": "Data Delete"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)