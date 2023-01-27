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
import base64

router=APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/load/")
#첫번째 인자가 기본 사진 두번째 인자가 배경 사진 
async def load_photo(file:UploadFile=File(...),file2:UploadFile=File(...), file3:UploadFile=File(...), type :Optional[str]=None, userId :Optional[int]=None, db: Session=Depends(get_db)):
    filename=f"{uuid.uuid4()}.jpeg"
    resultfilename=f"{filename}result.jpeg"


    if(type=="CHANGESTYLE"):
       content= changeStyle(file)
       post_bucket(content,resultfilename) 
       photo=models.Photo(user_id=userId,photo_name=filename,update_type=type, result_name=resultfilename)
       

    elif(type=="REMOVEBACKGROUND"):
        content= changeBackground(file,file2)
        post_bucket(content,resultfilename) 
        photo=models.Photo(user_id=userId,photo_name=filename,update_type=type, result_name=resultfilename)
        
    
    crud.create_images(db=db,image=photo)
    content2=await file3.read()
    post_bucket(content2,filename)
    if os.path.exists('./savefig_default.png'):
        os.remove('./savefig_default.png')

    # elif os.path.exists('./output.png'):
    #     os.remove('./output.png')

    
    return {"resultfilename":resultfilename}


@router.get("/download/")
async def download_photo(db: Session = Depends(get_db), userId: Optional[int]=None, photoId: Optional[int]=None):
    image=crud.get_photo(db=db, user_id=userId, photo_id=photoId)
    pull_bucket(image[0])
    return True
   


def changeBackground(img1: UploadFile=File(...), img2: UploadFile=File(...)):
# Load model

    if os.path.exists('./output.png'):
        os.remove('./output.png')


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

    #output 이름 난수로 변경
    Image.fromarray(out).save('output.png') # save result

    os.remove(f"{file_path1}.png")
    os.remove(f"{file_path2}.png")

    output= open("output.png", "rb")

  

    return output



def changeStyle(file: UploadFile=File(...)):


    

    if not os.path.exists('./temp'):
        os.mkdir('./temp')

    print(f"{file.filename}")

    file_path = "temp/"
    

    with open(f"{file_path}.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    picture(f"{file_path}.png")
    savefig_default= open("savefig_default.png", "rb")
    #
    
    os.remove(f"{file_path}.png")

    return savefig_default