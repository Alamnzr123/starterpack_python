# PART 1 - Alembic-FastAPI

This is simple init how to create data using Alembic ORM with FastAPI.
I separate 2 part which Part 1 : Init project and simple setup
Part 2 : More structure files and use Best Practice. 

![screenshot](ss.png)

## Set Up Project

1. clone repo `https://github.com/Alamnzr123/alembic-fastapi-part2`
2. Continue from `PART 1`
3. Install package: 
```
pip install databases
pip install databases[postgresql]
pip install asyncpg
```
4. Add `db.py`

```
import os
from databases import Database
from dotenv import load_dotenv
import sqlalchemy
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

db = Database(os.environ["DATABASE_URL"])
metadata = sqlalchemy.MetaData()
```

5. Add `app.py`

```
from db import db
from fastapi import FastAPI


app = FastAPI(title="Async FastAPI")


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
```

6. change `models.py`

```
import sqlalchemy
from db import db, metadata, sqlalchemy


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("age", sqlalchemy.Integer),
)


class User:
    @classmethod
    async def get(cls, id):
        query = users.select().where(users.c.id == id)
        user = await db.fetch_one(query)
        return user

    @classmethod
    async def create(cls, **user):
        query = users.insert().values(**user)
        user_id = await db.execute(query)
        return user_id
```

7. change `main.py`

```
import uvicorn
from models import User as ModelUser
from schema import User as SchemaUser
from app import app
from db import db


@app.post("/user/")
async def create_user(user: SchemaUser):
    user_id = await ModelUser.create(**user.dict())
    return {"user_id": user_id}


@app.get("/user/{id}", response_model=SchemaUser)
async def get_user(id: int):
    user = await ModelUser.get(id)
    return SchemaUser(**user).dict()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

we are using async/await

8. Modify Alembic config `alembic/env.py`

FROM 
```
import models

target_metadata = models.Base.metadata
```

TO 

```
import models
from db import metadata

target_metadata = metadata
```

9. make our first migration on PostgreSQL :

```
alembic revision --autogenerate -m "First migration"
```

10. run the migration :

```
alembic upgrade head
```

10. Run SERVER/APP :

```
uvicorn main:app
```

11. Open PGAdmin4 and find your DB
12. Open `http://127.0.0.1:8000/docs` FASTAPI SERVER to CREATE, GET data
or using POSTMAN
13. DONE.

* IGNORE THE `Pipfile` using pip package manager

## Package

alembic
fastAPI
Pydantic

## Programming Language
Python