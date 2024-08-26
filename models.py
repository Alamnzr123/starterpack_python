import sqlalchemy
from sqlalchemy.sql import func
from db import db, metadata, sqlalchemy
from fastapi import HTTPException


books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("publish_date", sqlalchemy.DateTime(timezone=True), server_default=func.now()),
    sqlalchemy.Column("author_id", sqlalchemy.String),
)


class Books:
    @classmethod
    async def get_all(cls):
        query = books.select()
        book = await db.fetch_all(query)
        return book

    @classmethod
    async def get_byId(cls, id):
        query = books.select().where(books.c.id == id)
        book = await db.fetch_one(query)

         # Check if id exists. If not, return 404 not found response
        if not book:
            raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
        return book

    @classmethod
    async def create(cls, **book):
        query = books.insert().values(**book)
        book_id = await db.execute(query)
        return book_id
    
    @classmethod
    async def update_books(cls, id, **book):
        query = books.select().where(books.c.id == id)
        get_book = await db.fetch_one(query)

        if get_book:
            query2 = books.update().values(**book)
            await db.execute(query2)

        # Check if id exists. If not, return 404 not found response
        if not get_book:
            raise HTTPException(status_code=404, detail=f"Task with id {id} not found")

        return get_book
    
    @classmethod
    async def delete_books(cls, id):
        query = books.delete().where(books.c.id == id)
        await db.fetch_one(query)
        