from fastapi import FastAPI,Response,status,HTTPException # type: ignore
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas,utils
from .database import engine,get_db 
from fastapi import Depends
models.Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import Session
from typing import List

from .routers import post,user,auth

app= FastAPI()


try:
    # Use f-strings for cleaner connection string construction
    connection_string = f"postgresql://postgres:1234@localhost/fastapi"

    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # Use correct cursor factory
    print("Database connection successful!")

except Exception as err:
    print(f"Error connecting to database: {err}")



my_posts=[{"id":1,"title":"post 1 title","content":"conntent of post 1","publish":True}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p

def find_post_index(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)






