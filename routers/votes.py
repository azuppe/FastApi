from email.policy import HTTP
from pyexpat import model
from signal import raise_signal
from sre_parse import State
from fastapi import FastAPI, status,  Response, HTTPException, Depends, APIRouter
from database import engine, get_db
import models
import schemas
import untils
from sqlalchemy.orm import Session
import oauth2


# models.Base.metadata.create_all(bind=engine)
router = APIRouter(
    prefix="/votes",
    tags=["Votes"]  # to group things
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(payload: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == payload.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found with id: {payload.post_id}")

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == payload.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if payload.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="User has already voted for this post")

        new_vote = models.Vote(post_id=payload.post_id,
                               user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Successfully removed vote"}
        print(payload)
