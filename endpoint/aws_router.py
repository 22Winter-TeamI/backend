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
async def load_photo(file:UploadFile=File(...), type :Optional[str]=None, user :Optional[int]=None, db: Session=Depends(get_db)):
    filename=f"{uuid.uuid4()}.jpeg"
    if(type=="CHANGESTYLE"):
       resultfilename= changeStyle(file)
       photo=models.UploadedPhoto(user_id=user,photo_name=filename,update_type=type, result_name=resultfilename)
    elif(type=="REMOVEBACKGROUND"):
        print("to be continue")
        # models.Photo(user_id=user,photo_name=filename,update_type=type, result_name=filename)
    crud.create_images(db=db,image=photo)
    content=await file.read()
    post_bucket(content,filename)
    return {"resultfilename":resultfilename}

# user_id와 photo_id로 받아오기
@router.get("/download/")
async def download_photo(db: Session = Depends(get_db), user: Optional[int]=None, id: Optional[int]=None):
    image=crud.get_photo(db=db, user_id=user, photo_id=id)
    pull_bucket(image[0])
    return image



def changeStyle(file: UploadFile=File(...)):
    if not os.path.exists('./temp'):
        os.mkdir('./temp')

    print(f"{file.filename}")

    file_path = "temp/"
    

    with open(f"{file_path}.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    IM =picture(f"{file_path}.png")
    resultfilename=f"{uuid.uuid4()}.jpeg"
    # a=cv2.imwrite('filename.jpeg', A)
 
    # A=Image.fromarray((IM * 1).astype(np.uint8)).convert('RGB')
    # # print(picture(f"{file_path}.png"))
    # content= A.read()
  
    post_bucket(bytearray(IM),resultfilename) 
  
    # print(content)
    # post_bucket(content,'savefig_default.png')  
    os.remove('./savefig_default.png')
    os.remove(f"{file_path}.png")
    # changedImage = FileResponse("./savefig_default.png")
    # print(changedImage)
    
    #return FileResponse("./savefig_default.png")
    return resultfilename