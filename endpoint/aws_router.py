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
from celery.result import ResultBase

router=APIRouter(
    prefix="/api/v1"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/")  ##user부분에 저는 get방식으로 username을 받아와서 id를 찾도록 만들었는데 이 코드는 post로 userid를 받아와서 둘중하나로 맞춰야 할 것 같아요
async def load_photo( user:Optional[int]=None, type :Optional[str]=None, file:UploadFile=File(...), db: Session=Depends(get_db)):
    filename=f"{uuid.uuid4()}.jpeg"
    if((type=="CHANGESTYLE")or(type=="REMOVEBACKGROUND")):
        photo=models.Photo(user_id=user,photo_name=filename,update_type=type)
    else:
        return {"status":400} #상태코드 바꾸기
         
    crud.create_images(db=db,image=photo)
    content=await file.read()
    # post_bucket(content,filename)
    task_id=ai.delay(filename)
    taskid=task_id.id
    print(task_id)
    print(task_id.backend)
    print(task_id.ready())
    print(task_id.result)
    print("------------------------------------------------------")
    print(celery.AsyncResult(taskid, app=celery).state)
    print(celery.AsyncResult(taskid, app=celery).ready())
    print(celery.AsyncResult(taskid, app=celery).get())
    print(celery.AsyncResult(taskid, app=celery).state)
    print(celery.AsyncResult(taskid, app=celery).state)
    print(celery.AsyncResult(taskid, app=celery).state)
    print(celery.AsyncResult(taskid, app=celery).state)


    # return task_id

    return {"taskid":f'${task_id}'}

# user_id와 photo_id로 받아오기 => 다운로드 안됨


@router.get("/download/{user_id}")
async def download_photo(db: Session = Depends(get_db), user_id: Optional[int]=None, id: Optional[int]=None):
    image=crud.get_photo(db=db, user_id=user_id, photo_id=id)
    pull_bucket(image[0])
    return image 

    

# def getresult(taskid:str,db: Session = Depends(get_db)):

@router.post("/photos")
def getresult(taskid :Optional[str]=None, user_id:Optional[int]=None,db: Session = Depends(get_db)):

    if((celery.AsyncResult(taskid).state)==SUCCESS):
        print(celery.AsyncResult(taskid, app=celery).state)
        
        print(celery.AsyncResult(taskid))
        print(celery.AsyncResult(taskid, app=celery).backend)
        # print(task.ready())
        # print(task.ready())
        print(celery.AsyncResult(taskid).get())
        print(celery.AsyncResult(taskid).result)
        print(celery.AsyncResult(taskid, app=celery).backend)
        # crud.get_photo(db=db, user_id=user_id, photo_id=id)
        return "success "

    elif((celery.AsyncResult(taskid).state)==PENDING):
        print(task.result)
        print(task.state)
        print(task.get())
        print(celery.AsyncResult(taskid))
        # print(task.ready())
        # print(task.ready())
        print(task.result)
        print(celery.AsyncResult(taskid, app=celery).backend)
        print(task.get())
        return "pending "
    else:
        return {"status":"???"}