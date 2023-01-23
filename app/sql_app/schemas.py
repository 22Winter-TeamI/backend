from pydantic import BaseModel
import enum

class EffectType(str,enum.Enum):
    rmbackground = "REMOVEBACKGROUND"
    style = "CHANGESTYLE"

class PhotoBase(BaseModel):
    class Config:
        orm_mode = True

class Photo(BaseModel):
    photo_id: int
    user_id: int
    photo_name: str
    result_name: str
    update_type: enum.Enum
    is_deleted:bool
    create_at: str
    update_at:str

class PhotoCreate(BaseModel):

    user_id: int
    photo_name: str
    update_type: enum.Enum
    
class UserBase(BaseModel): 
    class Config:
        orm_mode = True


# class User(BaseModel):
#     # user_id: int
#     name: str 
#     # create_at: str
#     # update_at:str

class UserID(BaseModel):
    user_id: int
    # name: str 
    # create_at: str
    # update_at:str

class UserName(BaseModel):
    # user_id: int
    name: str 
    # create_at: str
    # update_at:str

