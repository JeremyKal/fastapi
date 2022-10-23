from database import SessionLocal, Base, engine
import models
from sqlalchemy import orm
import schemas

from fastapi import Body, Depends, FastAPI, HTTPException, Request



def create_database():
    Base.metadata.create_all(bind=engine)
    

def get_db():
    #created in database.py
    db = SessionLocal()
    try:
        yield db
    finally:
        #always close the session
        db.close()
        
        
# --------------------TOKENS

def get_blacklisted_tokens(db: orm.Session):
    return db.query(models.TokenBlacklist).all()
        
        
def check_token_blacklist(db: orm.Session, request: Request):
    token = request.headers["authorization"].split()[1]
    blacklisted_token = db.query(models.TokenBlacklist).filter(models.TokenBlacklist.token == token).first()
    if blacklisted_token:
        raise HTTPException(status_code=403, detail="Token is blacklisted. Need new authentication")



# -------------------USERS

def get_user_by_email(db: orm.Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: orm.Session, user: schemas.UserCreate):
    # password needs to be hashed to be stored in db
    not_really_hashed_password = user.password + "fakehashed"
    db_user = models.User(email=user.email, hashed_password=not_really_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: orm.Session, skip: int, limit: int):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(db: orm.Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# ------------------- ACCOUNT

def check_user(db: orm.Session, user: schemas.UserCreate):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        is_password_valid = user.password + "fakehashed" == db_user.hashed_password
        return is_password_valid
    return False


def blacklist_token(db: orm.Session, token: str):
    blacklisted_token = models.TokenBlacklist(token=token)
    db.add(blacklisted_token)
    db.commit()
    db.refresh(blacklisted_token)

# -------------------POSTS

def create_post(db: orm.Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(title=post.title, content=post.content, owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: orm.Session, skip: int, limit:int):
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_post_by_id(db: orm.Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def delete_post_by_id(db: orm.Session, post_id: int):
    db_post = get_post_by_id(db=db, post_id=post_id)
    db.delete(db_post)
    db.commit()
    

def update_post_by_id(db: orm.Session, post_id: int, post: schemas.PostCreate, db_post: models.Post):
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post
