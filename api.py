from fastapi import APIRouter
from endpoint import awsphoto_load

api_router = APIRouter()

api_router.include_router(awsphoto_load.router, prefix="/photoload", tags=["awsphoto_load"])
