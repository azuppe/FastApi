
import untils
import models
import schemas
import oauth2
from database import get_db
from sqlalchemy.orm import Session
from sre_parse import State
from fastapi import Depends, APIRouter, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(payload: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == payload.username).first()

#OAuth2PasswordRequestForm returns {username:"some text here", password:"Some text here"}

#should senf form data


    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid email or password")
    if not untils.verify(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid email or password")

    # create a token
    # return a token
    access_token = oauth2.create_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
