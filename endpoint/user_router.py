from fastapi import APIRouter, Depends, HTTPException
from app.aws.bucket import *
from sqlalchemy.sql import func
from app.sql_app import crud, schemas
from sqlalchemy.orm import Session
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from database import SessionLocal

router=APIRouter( prefix="/api/v1")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/")
def create_user(user: schemas.UserName, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        return {"status":200}

    return crud.create_user(db=db, user=user)


@router.get("/image/{user_id}")
def read_gallery(user_id: int, db: Session = Depends(get_db)):
    # user_id=crud.get_user_name_from_user_id(db,user_name=user_name)
    # print(user_id)
    db_user_url = crud.get_user_images(db, user_id=user_id)
    if db_user_url is None:
        raise HTTPException(status_code=404, detail="no register photo")

    return db_user_url

@router.get("/image/background/{user_id}")
def read_gallery_rmback(user_id: int, db: Session = Depends(get_db)):
    db_user_url = crud.get_user_images_rmbackgournd(db, user_id=user_id)
    if db_user_url is None:
        raise HTTPException(status_code=404, detail="no register photo")

    return db_user_url

@router.get("/image/paint/{user_id}")
def read_gallery_paint(user_id: int, db: Session = Depends(get_db)):
    db_user_url = crud.get_user_images_paint(db, user_id=user_id)
    if db_user_url is None:
        raise HTTPException(status_code=404, detail="no register photo")

    return db_user_url
