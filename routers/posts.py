# fetch all posts
from pyexpat import model
from fastapi import FastAPI, status,  Response, HTTPException, Depends, APIRouter
from typing import List, Optional
from database import engine, get_db
import models
import schemas
import oauth2
from sqlalchemy import func

from sqlalchemy.orm import Session

# models.Base.metadata.create_all(bind=engine)
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]  # to group things in the doc
)


# @router.get("/", )
@router.get("/", response_model=List[schemas.VoteOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search:Optional[str]=""):
    # print(schemas.VoteOut.Post)
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results  = db.query(models.Post, func.count(models.Vote.post_id).label ("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #by default sqp alchamy uses inner left join

    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(payload: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user)

    new_post = models.Post(owner_id=current_user.id, **payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''',
    #                (payload.title, payload.content, payload.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    return new_post


@router.get("/{id}",  response_model=schemas.VoteOut)
def fetch_posts(id: int, db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM posts WHERE id = %s ''', (str(id),))
    # post = cursor.fetchone()
    # print(post)

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    results  = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found with id: {id}")

    return results


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     '''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found with id: {id}")

    if deleted_post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorised to delete this post")

    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",  response_model=schemas.PostResponse)
def update_posts(id: int, payload: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # print(Post)
    # cursor.execute('''UPDATE posts SET title = %s, content = %s, published=%s WHERE id = %s RETURNING * ''',
    #                (payload.title, payload.content, payload.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found with id: {id}")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorised to delete this post")

    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
