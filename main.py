from fastapi import Depends, HTTPException,FastAPI
from app.aws.bucket import *
from sqlalchemy.sql import func
from starlette.middleware.cors import CORSMiddleware
from app.sql_app import models
# from sql_app.crud import *
# # import schemas,models,crud
from database import SessionLocal, engine
from endpoint import aws_router, user_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(aws_router.router)
app.include_router(user_router.router)

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

# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


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


