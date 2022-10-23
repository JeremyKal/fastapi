from typing import List
import os
from fastapi import Body, Depends, FastAPI, HTTPException, Request, responses
from sqlalchemy import orm

from auth.jwt_bearer import JwtBearer
# PostSchema, UserSchema, UserLoginSchema, 
from auth.jwt_handler import signJWT
import schemas
import services
from fastapi.staticfiles import StaticFiles


app = FastAPI()
services.create_database()

# -------------------------- ACCOUNT

#POST account/register
@app.post("/account/register", tags=["Account"])
def register(user: schemas.UserCreate = Body(default=None), db:orm.Session = Depends(services.get_db)):
    db_user = services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    created_user = services.create_user(db=db, user=user)
    return signJWT(created_user.email)

#POST account/login
@app.post("/account/login", tags=["Account"])
def login(user: schemas.UserCreate = Body(default=None), db:orm.Session = Depends(services.get_db)):
    if not services.check_user(db=db, user=user):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return signJWT(user.email)


#POST account/logout
@app.post("/account/logout", dependencies=[Depends(JwtBearer())], tags=["Account"])
def logout(db:orm.Session = Depends(services.get_db), request: Request = None):
    jwt_token = request.headers["authorization"].split()[1]
    services.blacklist_token(db=db, token=jwt_token)
    return {"message": "Logged out successfully, token blacklisted"}


@app.get("/account/blacklisted-tokens", tags=["Account"])
def get_blacklisted_tokens(db:orm.Session = Depends(services.get_db)):
    return services.get_blacklisted_tokens(db=db)


# -------------------------- USERS

@app.post("/users/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db:orm.Session = Depends(services.get_db)):
    #first check if user email already exists
    db_user = services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    # service methode important
    return services.create_user(db=db, user=user)
    
    
@app.get("/users/", response_model=List[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 10, db:orm.Session = Depends(services.get_db)):
    return services.get_users(db=db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def read_user(user_id: int, db:orm.Session = Depends(services.get_db)):
    db_user = services.get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# -------------------------- POSTS

@app.post("/users/{user_id}/posts/", dependencies=[Depends(JwtBearer())], response_model=schemas.Post, tags=["Posts"])
def create_post(user_id: int, post: schemas.PostCreate, db:orm.Session = Depends(services.get_db), request: Request = None):
    services.check_token_blacklist(request=request, db=db)
    db_user = services.get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return services.create_post(db=db, post=post, user_id=user_id)


@app.get("/posts/", dependencies=[Depends(JwtBearer())], response_model=List[schemas.Post], tags=["Posts"])
def read_posts(skip: int = 0, limit: int = 10, db:orm.Session = Depends(services.get_db), request: Request = None):
    services.check_token_blacklist(request=request, db=db)
    return services.get_posts(db=db, skip=skip, limit=limit)


@app.get("/posts/{post_id}", dependencies=[Depends(JwtBearer())], response_model=schemas.Post, tags=["Posts"])
def read_post(post_id: int, db:orm.Session = Depends(services.get_db), request: Request = None):
    services.check_token_blacklist(request=request, db=db)
    db_post = services.get_post_by_id(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.delete("/posts/{post_id}", dependencies=[Depends(JwtBearer())], tags=["Posts"])
def delete_post(post_id: int, db:orm.Session = Depends(services.get_db), request: Request = None):
    services.check_token_blacklist(request=request, db=db)
    db_post = services.get_post_by_id(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    services.delete_post_by_id(db=db, post_id=post_id)
    return {"message": f"Post with id {post_id} deleted"}


@app.put("/posts/{post_id}", dependencies=[Depends(JwtBearer())], response_model=schemas.Post, tags=["Posts"])
def update_post(post_id: int, post: schemas.PostCreate, db:orm.Session = Depends(services.get_db), request: Request = None):
    services.check_token_blacklist(request=request, db=db)
    db_post = services.get_post_by_id(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return services.update_post_by_id(db=db, post_id=post_id, post=post, db_post=db_post)


#-------------------------- STATIC FILES

app.mount("/static/html", StaticFiles(directory="static"), name="static")

@app.get("/static/images/{image_name}", tags=["Static Images"])
def get_static_image(image_name: str):
    return responses.FileResponse(f"static/images/{image_name}", media_type="image/png", filename=image_name)



# posts = [
#     {
#         "id": 1,
#         "title": "title 1",
#         "content": "content 1"
#     },
#     {
#         "id": 2,
#         "title": "title 2",
#         "content": "content 2"
#     },
#     {
#         "id": 3,
#         "title": "title 3",
#         "content": "content 3"
#     },
# ]

# users = []

# @app.get("/", tags=["Home"])
# def root():
#     return {"message": "Hello World"}
  

# # GET /posts
# @app.get("/posts", tags=["Post"])
# def get_posts():
#     return {"data": posts}


# # GET /posts/{id}
# @app.get("/posts/{id}", tags=["Post"])
# def get_post(id: int):
#     post = [post for post in posts if post["id"] == id]
#     if len(post):
#         return {"data": post[0]}
#     return {"message": "Post not found !"}


# #POST /posts
# @app.post("/posts", dependencies=[Depends(JwtBearer())], tags=["Post"])
# def add_post(post: PostSchema):
#     post.id = len(posts) + 1
#     posts.append(post.dict())
#     return {"message": "Post added successfully"}


# #POST user/register
# @app.post("/user/register", tags=["User"])
# def register(user: UserSchema = Body(default=None)):
#     users.append(user.dict())
#     return signJWT(user.email)

# def check_user(data: UserLoginSchema):
#     for user in users:
#         if user["email"] == data.email and user["password"] == data.password:
#             return True
#     return False


# #POST user/login
# @app.post("/user/login", tags=["User"])
# def login(user: UserLoginSchema = Body(default=None)):
#     if check_user(user):
#         return signJWT(user.email)
#     return {"message": "Invalid credentials"}
