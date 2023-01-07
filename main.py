from fastapi import File, UploadFile, Depends, HTTPException,FastAPI,Depends
from app.aws.bucket import *
from sqlalchemy.sql import func
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.sql_app import crud, models, schemas
# from sql_app.crud import *
# # import schemas,models,crud
from .database import SessionLocal, engine
import uuid
from typing import Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"message": "Hello World"}

###########################################

@app.post("/load")
async def load_photo(file:UploadFile=File(...), type :Optional[str]=None, user :Optional[str]=None):
    file.filename=f"{type}_{user}_{uuid.uuid4()}.jpeg"
    content=await file.read()
    post_bucket(content,file.filename)
    return {"image_name:":file.filename, "type:":type, "user:":user}

@app.get("/download")
async def download_photo(filename:str):
    pull_bucket(filename)

####################################
@app.post("/users/")
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="name already registered")

    return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
   
    db_user = crud.get_user(db, user_id=user_id)
    print("-------------------------")
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print("\n-------------------------")
    print(db_user)
    print("\n-------------------------")
    print(db_user.name)
    return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items

# @app.get("/images")
# def gallery_all_user(user_name: str, db: Session = Depends(get_db)):
#     get_photos = crud.get_photos(db, user_name=user_name)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     return db_user


