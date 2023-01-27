from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from transparent_background import Remover

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
from fastapi.responses import FileResponse
import shutil
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from ai.code import picture
from PIL import Image
import numpy as np
import cv2 

router=APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/load/")
async def load_photo(file:UploadFile=File(...), type :Optional[str]=None, userId :Optional[int]=None, db: Session=Depends(get_db)):
    filename=f"{uuid.uuid4()}.jpeg"
    if(type=="CHANGESTYLE"):
       resultfilename= changeStyle(file)
       photo=models.Photo(user_id=userId,photo_name=filename,update_type=type, result_name=resultfilename)
    elif(type=="REMOVEBACKGROUND"):
        print("to be continue")
        # models.Photo(user_id=user,photo_name=filename,update_type=type, result_name=filename)
    crud.create_images(db=db,image=photo)
    content=await file.read()
    post_bucket(content,filename)
    return {"resultfilename":resultfilename}


@router.get("/download/")
async def download_photo(db: Session = Depends(get_db), userId: Optional[int]=None, photoId: Optional[int]=None):
    image=crud.get_photo(db=db, user_id=userId, photo_id=photoId)
    pull_bucket(image[0])
    return image


@router.post("/changeBackground")
def changeBackground(img1: UploadFile=File(...), img2: UploadFile=File(...)):
# Load model
    
    remover = Remover() # default setting
    remover = Remover(fast=True, jit=True, device='cpu') # custom setting


    if not os.path.exists('./temp1'):
        os.mkdir('./temp1')

    file_path1 = "temp1/"

    with open(f"{file_path1}.png", "wb") as buffer:
        shutil.copyfileobj(img1.file, buffer)

    # Usage for image
    img = Image.open(f"{file_path1}.png").convert('RGB') # read image

    if not os.path.exists('./temp2'):
        os.mkdir('./temp2')

    file_path2 = "temp2/"

    with open(f"{file_path2}.png", "wb") as buffer:
        shutil.copyfileobj(img2.file, buffer)
        
    out = remover.process(img, type=f"{file_path2}.png") # use another image as a background

    Image.fromarray(out).save('output.png') # save result

    os.remove(f"{file_path1}.png")
    os.remove(f"{file_path2}.png")

    return FileResponse("./output.png")



def changeStyle(file: UploadFile=File(...)):
    if not os.path.exists('./temp'):
        os.mkdir('./temp')

    print(f"{file.filename}")

    file_path = "temp/"
    

    with open(f"{file_path}.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    IM =picture(f"{file_path}.png")
    resultfilename=f"{uuid.uuid4()}.jpeg"
    post_bucket(bytearray(IM),resultfilename) 
    os.remove('./savefig_default.png')
    os.remove(f"{file_path}.png")

    return resultfilename