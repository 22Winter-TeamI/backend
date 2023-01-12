from fastapi import APIRouter, Depends, HTTPException
from app.aws.bucket import *
from sqlalchemy.sql import func
from app.sql_app import crud, schemas
from sqlalchemy.orm import Session
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from database import SessionLocal

router=APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/")
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="name already registered")

    return crud.create_user(db=db, user=user)

@router.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
   
    db_user = crud.get_user(db, user_id=user_id)
    print("-------------------------")
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print("\n-------------------------")
    print(db_user)
    print("\n-------------------------")
    print(db_user.name)
    return db_user
