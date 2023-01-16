from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from app.aws.bucket import *
from sqlalchemy.sql import func
import uuid
from typing import Optional
from app.sql_app import crud, schemas, models
from sqlalchemy.orm import Session
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from database import SessionLocal

router=APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/load/")
async def load_photo(file:UploadFile=File(...), type :Optional[str]=None, user :Optional[int]=None, db: Session=Depends(get_db)):
    filename=f"{type}_{user}_{uuid.uuid4()}.jpeg"
    if((type=="CHANGESTYLE")or(type=="REMOVEBACKGROUND")):
        photo=models.UploadedPhoto(user_id=user,photo_name=filename,update_type=type, result_name=filename)
    else:
        photo=models.UploadedPhoto(user_id=user,photo_name=filename, result_name=filename)
    crud.create_images(db=db,image=photo)
    content=await file.read()
    post_bucket(content,filename)
    return filename, type, user

# user_id와 photo_id로 받아오기
@router.get("/download/")
async def download_photo(db: Session = Depends(get_db), user: Optional[int]=None, id: Optional[int]=None):
    image=crud.get_photo(db=db, user_id=user, photo_id=id)
    pull_bucket(image[0])
    return image

# result_name으로 받아오기
# @router.get("/download/")
# async def download_photo(db: Session = Depends(get_db), image_name:Optional[str]=None):
#     pull_bucket(image_name)
#     return image_name