from fastapi import Depends, HTTPException,FastAPI
from app.aws.bucket import *
from sqlalchemy.sql import func
from starlette.middleware.cors import CORSMiddleware
from app.sql_app import models
# from sql_app.crud import *
# # import schemas,models,crud
from database import SessionLocal, engine
from endpoint import aws_router, user_router
from prometheus_fastapi_instrumentator import Instrumentator

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



@app.get("/")
async def root():
    return {"message": "Hello World"}

Instrumentator().instrument(app).expose(app)