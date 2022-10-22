from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Settings


settings = Settings()


# SQLALCHEMY_DATABASE_URL = postgresql://<username>:<password>@< ip addresss/ hostname>/<db name>
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





# while True:

#     try:
#         conn = psycopg2.connect(host="localhost", database="post_app",
#                                 user="postgres", password="azuPPE#123", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Databse connection was successful")
#         break
#     except Exception as error:
#         print("Could not connect to postgres database")
#         print(error)
#         time.sleep(4)


