from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime,Enum
from sqlalchemy.orm import relationship
import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import database
from database import Base
from sqlalchemy.sql import func
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from sql_app.schemas import EffectType

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(20),unique=True)
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at =Column(DateTime(timezone=True), default=func.now())
    # uploadedphoto = relationship("UploadedPhoto", backref="user")


class UploadedPhoto(Base):
    __tablename__ = "uploadedphoto"

    photo_id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey('user.user_id'))
    origin_url = Column(String(100), unique=True)
    background_url=Column(String(100), unique=True)
    update_type = Column(Enum(EffectType))
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at =Column(DateTime(timezone=True), default=func.now())
    # user = relationship("TbUser", backref=backref("addresses", order_by=id))



class ResultPhoto(Base):
    __tablename__ = "resultphoto"

    result_photo = Column(Integer, primary_key=True,autoincrement=True )
    photo_id = Column(Integer, ForeignKey('uploadedphoto.photo_id'),unique=True, nullable=False)
    result_url= Column(Integer, unique=True, nullable=False)
    create_at = Column(DateTime(timezone=True), default=func.now())
    update_at =Column(DateTime(timezone=True), default=func.now())
    is_deleted=Column(Boolean,default=True)


