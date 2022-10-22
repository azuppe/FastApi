
from fastapi import FastAPI, status,  Response, HTTPException, Depends, APIRouter
from app.database import engine, get_db
import app.models as models, app.schemas as schemas, app.untils as untils
from sqlalchemy.orm import Session



# models.Base.metadata.create_all(bind=engine)
router = APIRouter(
    prefix="/users",
    tags=["Users"] # to group things 
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_users(payload: schemas.CreateUser, db: Session = Depends(get_db)):

    #hash passsword
    hashed_password = untils.hash(payload.password)
    payload.password = hashed_password
    new_user = models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}",  response_model=schemas.UserResponse)
def fetch_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user found with id: {id}")

    return user

