from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from app.aws.bucket import *
from sqlalchemy.sql import func
from app.sql_app import crud, schemas
from sqlalchemy.orm import Session
import os
import sys
import base64
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from database import SessionLocal

from PIL import Image
import requests
import shutil




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
    

@router.get("/image/{userName}")
def read_gallery(userName: str, db: Session = Depends(get_db)):
    userId=crud.get_user_name_from_user_id(db,user_name=userName)

    db_user_url = crud.get_user_images(db, user_id=userId)
    if db_user_url is None:
        raise HTTPException(status_code=404, detail="no register photo")

    return db_user_url


@router.get("/image/origin/{userName}")
def read_gallery(userName: str, db: Session = Depends(get_db)):
    userId=crud.get_user_name_from_user_id(db,user_name=userName)

    db_user_url = crud.get_origin_photo(db, user_id=userId)
    print(db_user_url)
    
    if db_user_url is None:
        raise HTTPException(status_code=404, detail="no register photo")
    
    some_file_path = db_user_url[0]
    
    response = requests.get(some_file_path, stream=True)
    
    with open('my_image.png', 'wb') as buffer:
        shutil.copyfileobj(response.raw, buffer)
        
    del response
    
    picture = FileResponse('my_image.png')
    return picture

@router.get("/image/result/{userName}")
def read_gallery(userName: str, db: Session = Depends(get_db)):
    userId=crud.get_user_name_from_user_id(db,user_name=userName)

    db_user_url = crud.get_result_photo(db, user_id=userId)
    
    if db_user_url is None:
        raise HTTPException(status_code=404, detail="no register photo")
    
    some_file_path = db_user_url[0]
    
    response = requests.get(some_file_path, stream=True)
    
    with open('my_image1.png', 'wb') as buffer:
        shutil.copyfileobj(response.raw, buffer)
    del response
    
    picture = FileResponse('my_image1.png')
    
    return picture
    # img = FileResponse(some_file_path)
    # return img

@router.get("/image/background/{userName}")
def read_gallery_rmback(userName: str, db: Session = Depends(get_db)):
    userId=crud.get_user_name_from_user_id(db,user_name=userName)
    db_user_url = crud.get_user_images_rmbackgournd(db, user_id=userId)
    if db_user_url is None:
        raise HTTPException(status_code=404, detail="no register photo")

    return db_user_url

@router.get("/image/paint/{userName}")
def read_gallery_paint(userName: str, db: Session = Depends(get_db)):
    userId=crud.get_user_name_from_user_id(db,user_name=userName)
    db_user_url = crud.get_user_images_paint(db, user_id=userId)
    if db_user_url is None:
        raise HTTPException(status_code=404, detail="no register photo")

    return db_user_url
