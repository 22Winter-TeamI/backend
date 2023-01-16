from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime,Enum
from sqlalchemy.orm import relationship
import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from database import Base
from sqlalchemy.sql import func
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from sql_app.schemas import EffectType

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(20),unique=True)
    email = Column(String(50),unique=True)
    is_deleted=Column(Boolean,default=False)
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at =Column(DateTime(timezone=True), default=func.now())
    
    uploadedphoto=relationship("UploadedPhoto", back_populates="users")


class UploadedPhoto(Base):
    __tablename__ = "uploadedphoto"

    photo_id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey('user.user_id'))
    photo_name = Column(String(255), unique=True)
    result_name= Column(String(255), unique=True)
    is_deleted=Column(Boolean,default=False)
    update_type = Column(Enum(EffectType))
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at =Column(DateTime(timezone=True), default=func.now())
    
    users = relationship("User", back_populates="uploadedphoto")