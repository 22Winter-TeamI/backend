from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from endpoint import awsphoto_load
from api import api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(awsphoto_load.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}