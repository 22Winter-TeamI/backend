from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from aws.bucket import *
from sqlalchemy.sql import func
import uuid
from typing import Optional

router=APIRouter()

@router.post("/load")
async def load_photo(file:UploadFile=File(...), type :Optional[str]=None, user :Optional[str]=None):
    file.filename=f"{type}_{user}_{uuid.uuid4()}.jpeg"
    content=await file.read()
    post_bucket(content,file.filename)
    return {"image_name:":file.filename, "type:":type, "user:":user}

@router.get("/download")
async def download_photo(filename:str):
    pull_bucket(filename)