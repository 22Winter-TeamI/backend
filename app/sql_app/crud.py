from sqlalchemy.orm import Session

from . import models, schemas
from sqlalchemy import and_

#is_deleted라면 없는 이름이라고 뜨기
def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def create_user(db: Session, user: str):
   
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
 
def get_user_name_from_user_id(db: Session, user_name: str):
    a= db.query(models.User.user_id).filter(models.User.name == user_name).first()
    b=int(str(a).strip('(').strip(')').strip(','))
    return b

def get_user_images(db: Session, user_id: str):
    photo_ids= db.query(models.UploadedPhoto.result_name,models.UploadedPhoto.photo_name).filter(models.UploadedPhoto.user_id == user_id).all()
    
    return photo_ids

def get_user_images_rmbackgournd(db: Session, user_id: str):
    photo_ids= db.query(models.UploadedPhoto.result_name,models.UploadedPhoto.photo_name).filter(and_(models.UploadedPhoto.user_id == user_id,models.UploadedPhoto.update_type== "REMOVEBACKGROUND")).all()

    return photo_ids

def get_user_images_paint(db: Session, user_id: str):
    photo_ids= db.query(models.UploadedPhoto.result_name,models.UploadedPhoto.photo_name).filter(and_(models.UploadedPhoto.user_id == user_id,models.UploadedPhoto.update_type== "CHANGESTYLE")).all()

    return photo_ids