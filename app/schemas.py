# equivalent to Django serializers

from pydantic import BaseModel, Field, EmailStr
from typing import List


# ------------------------- Post -------------------------

class PostBase(BaseModel):
    title: str
    content: str
    
    
class PostCreate(PostBase):
    pass


# reading post
class Post(PostBase):
    id: int
    owner_id: int
    
    class Config:
        # when loaing user, we want post to come with it
        orm_mode = True
        # example data shape
        schema_extra = {
            "post_demo": {
                "id": 1,
                "title": "Post title",
                "content": "this is the content",
                "owner_id": 1,
            }
        }

# ------------------------- User -------------------------

class UserBase(BaseModel):
    email: EmailStr
    
    
class UserCreate(UserBase):
    password: str 
    

# reading user
class User(UserBase):
    id: int
    is_active: bool
    posts: List[Post] = []
    
    class Config:
        orm_mode = True
        schema_extra = {
             "user_demo": {
                "email": "email1@test.fr",
                "id": 1,
                "is_active": True,
                "posts": []
            }
        }

# --------------------------

# class PostSchema(BaseModel):
#     id: int = Field(default=None)
#     title: str = Field(default=None)
#     content: str = Field(default=None)
    
#     class Config:
#         schema_extra = {
#             "post_demo": {
#                 "title": "Post title",
#                 "content": "this is the content"
#             }
#         }
        
        
# class UserSchema(BaseModel):
#     # id: int = Field(default=None)
#     username: str = Field(default=None)
#     email: EmailStr = Field(default=None)
#     password: str = Field(default=None)
    
#     class Config:
#         schema_extra = {
#             "user_demo": {
#                 "username": "user1",
#                 "email": "email1@test.fr",
#                 "password": "azerty1234",
#             }
#         }
        
        
# class UserLoginSchema(BaseModel):
#     email: EmailStr = Field(default=None)
#     password: str = Field(default=None)
    
#     class Config:
#         schema_extra = {
#             "user_demo": {
#                 "email": "email1@test.fr",
#                 "password": "azerty1234",
#             }
#         }