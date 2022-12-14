
from fastapi import FastAPI
from .routers import posts, users, votes 
import app.auth as auth
from app.config import Settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

settings = Settings()

origins =["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
@app.get("/")
def read_root():
    return {"Hello": "welcome to fastapi"}
