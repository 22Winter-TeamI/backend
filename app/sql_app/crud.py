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
    id= db.query(models.User.user_id).filter(models.User.name == user_name).first()
    return int(str(id).strip('(').strip(')').strip(','))


def get_user_images(db: Session, user_id: str):
    photo_ids= db.query(models.Photo.result_name,models.Photo.photo_name).filter(models.Photo.user_id == user_id).all()
    
    return photo_ids

def get_user_images_rmbackgournd(db: Session, user_id: str):
    photo_ids= db.query(models.Photo.result_name,models.Photo.photo_name).filter(and_(models.Photo.user_id == user_id,models.Photo.update_type== "REMOVEBACKGROUND")).all()

    return photo_ids

def get_user_images_paint(db: Session, user_id: str):
    photo_ids= db.query(models.Photo.result_name,models.Photo.photo_name).filter(and_(models.Photo.user_id == user_id,models.Photo.update_type== "CHANGESTYLE")).all()

    return photo_ids

def get_user_images_origin(db: Session, user_id: str):
    photo_ids= db.query(models.Photo.result_name,models.Photo.photo_name).filter(and_(models.Photo.user_id == user_id,models.Photo.update_type== "CHANGESTYLE")).all()

    return photo_ids

def create_images(db:Session, image: schemas.PhotoCreate):
    db.add(image)
    db.commit()
    db.refresh(image)

def get_photo(db:Session, user_id:int, photo_id=int):
    photo_name=db.query(
        #photo_name-> result네임
        models.Photo.result_name).filter(
            and_(models.Photo.user_id==user_id,models.Photo.photo_id==photo_id)).first()
    
    return photo_name