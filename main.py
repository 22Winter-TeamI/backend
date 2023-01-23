from fastapi import Depends, HTTPException,FastAPI
from app.aws.bucket import *
from sqlalchemy.sql import func
from starlette.middleware.cors import CORSMiddleware
from app.sql_app import models
# from sql_app.crud import *
# # import schemas,models,crud
from database import SessionLocal, engine
from endpoint import aws_router, user_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(aws_router.router)
app.include_router(user_router.router)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## post 이미지 업로드 ->  셀러리 함수를 실행시키고 -> -> 디비에 결과값 저장 ->리턴은 task id로 준다

##get -> taskid 를 주면 상태를 요청하고 만약 상태가 success이면 -> 리턴으로  결과 url가져오기


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
