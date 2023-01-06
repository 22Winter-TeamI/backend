from fastapi import APIRouter, File, UploadFile, Depends, HTTPException

from aws.bucket import *
from sqlalchemy.sql import func
import uuid

router=APIRouter()

@router.post("/load")
async def load_photo(file:UploadFile=File(...),):
    file.filename=f"{uuid.uuid4()}.jpeg"
    content=await file.read()
    post_bucket(content,file.filename)

@router.get("/download")
async def download_photo(filename:str):
    pull_bucket(filename)