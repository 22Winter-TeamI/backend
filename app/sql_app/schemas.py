from pydantic import BaseModel
import enum

class ResultPhotoBase(BaseModel): 
    class Config:
        orm_mode = True

class ResultPhoto(BaseModel):
    result_photo: int
    photo_id: int 
    result_url: int
    create_at: str
    update_at: str
    is_deleted: bool

class EffectType(str,enum.Enum):
    rmbackground = "REMOVEBACKGROUND"
    style = "CHANGESTYLE"

class UploadedPhotoBase(BaseModel): 
    class Config:
        orm_mode = True

class ResultPhoto(BaseModel):
    photo_id: int
    user_id: int 
    origin_url: int
    background_url: str
    update_type: enum.Enum
    create_at: str
    update_at:str
    
class UserBase(BaseModel): 
    class Config:
        orm_mode = True


class User(BaseModel):
    # user_id: int
    name: str 
    # create_at: str
    # update_at:str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    username: str