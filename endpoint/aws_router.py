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

from ai.code import ai

from celery import Celery
from celery.result import AsyncResult
from celery.states import state, PENDING, SUCCESS
from ai.code import celery

router=APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/load/")  ##user부분에 저는 get방식으로 username을 받아와서 id를 찾도록 만들었는데 이 코드는 post로 userid를 받아와서 둘중하나로 맞춰야 할 것 같아요
async def load_photo( type :Optional[str]=None, user :Optional[int]=None, file:UploadFile=File(...), db: Session=Depends(get_db)):
    filename=f"{type}_{user}_{uuid.uuid4()}.jpeg"
    if((type=="CHANGESTYLE")or(type=="REMOVEBACKGROUND")):
        photo=models.UploadedPhoto(user_id=user,photo_name=filename,update_type=type)
    else:
        return {"status":400} #상태코드 바꾸기 
    crud.create_images(db=db,image=photo)
    content=await file.read()
    post_bucket(content,filename)
    task_id=ai.delay(filename)
    print(task_id)
    print(task_id.backend)
    print(task_id.ready())
    return {"taskid":f'${task_id}'}

# user_id와 photo_id로 받아오기
@router.get("/download/")
async def download_photo(db: Session = Depends(get_db), user: Optional[int]=None, id: Optional[int]=None):
    image=crud.get_photo(db=db, user_id=user, photo_id=id)
    pull_bucket(image[0])
    return image

    

# def getresult(taskid:str,db: Session = Depends(get_db)):

@router.post("/getresult")
def getresult(taskid :Optional[str]=None):
    task=AsyncResult(taskid)
    if((celery.AsyncResult(taskid, app=celery).state)==SUCCESS):
        # return crud.get_photo(db=db, user_id=user, photo_id=id)
        return "success "

    elif((AsyncResult(taskid).state)==PENDING):
       
        print(task.ready())
        print(task.result())
        print(celery.AsyncResult(taskid, app=celery).backend)
        print(task.get())
        
        
        # print(celery.AsyncResult(taskid, app=celery).get())
        return "pending "
    else:
        return {"status":"???"}