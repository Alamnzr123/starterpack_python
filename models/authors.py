import sqlalchemy
from db import db, metadata, sqlalchemy
from fastapi import HTTPException

authors = sqlalchemy.Table(
    "authors",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("bio", sqlalchemy.String),
    sqlalchemy.Column("birth_date", sqlalchemy.String),
)


class Authors:
    @classmethod
    async def get_all(cls):
        query = authors.select()
        author = await db.fetch_all(query)
        return author

    @classmethod
    async def get_byId(cls, id):
        query = authors.select().where(authors.c.id == id)
        author = await db.fetch_one(query)

         # Check if id exists. If not, return 404 not found response
        if not author:
            raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
        return author

    @classmethod
    async def create(cls, **author):
        query = authors.insert().values(**author)
        author_id = await db.execute(query)
        return author_id
    
    @classmethod
    async def update_authors(cls, id, **author):
        query = authors.select().where(authors.c.id == id)
        get_author = await db.fetch_one(query)

        if get_author:
            query2 = authors.update().values(**author)
            await db.execute(query2)

        # Check if id exists. If not, return 404 not found response
        if not get_author:
            raise HTTPException(status_code=404, detail=f"Task with id {id} not found")

        return get_author
    
    @classmethod
    async def delete_authors(cls, id):
        query = authors.delete().where(authors.c.id == id)
        await db.fetch_one(query)
        