
from fastapi import FastAPI,Response,status,HTTPException,APIRouter # type: ignore
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from .. import models, schemas,utils,oauth2
from ..database import engine,get_db 
from fastapi import Depends
models.Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import Session
from typing import List

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.PostResponse])
async def root(db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""select * from posts""")
    # all_posts=cursor.fetchall()
    all_posts=db.query(models.Post).filter(models.Post.owner_id==get_current_user.id).all()
    return all_posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
async def create_posts(new_post:schemas.PostCreate,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) """,(new_post.title,new_post.content,new_post.published))
    # conn.commit()
    post=models.Post(owner_id=get_current_user.id,**new_post.dict())
    print(get_current_user.email)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/{id}",response_model=schemas.PostResponse)
async def get_post(id,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):

    new_post=db.query(models.Post).filter(models.Post.id==id).first()
    return new_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id=%s returning * """,str(id))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    delete_post=db.query(models.Post).filter(models.Post.id==id)
    print(get_current_user.id)
    if delete_post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id not found")
    if delete_post.first().owner_id!=get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authorized to perform the actions")
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,id))
    # update_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)    
    update_post=post_query.first()
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post with id not exist")
    if update_post.owner_id!=get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authorized to perform the actions")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {"data":post_query.first()}

