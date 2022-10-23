import sqlalchemy as sql
from sqlalchemy import orm
from database import Base


class User(Base):
    __tablename__ = "users"
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    email = sql.Column(sql.String, unique=True, index=True)
    hashed_password = sql.Column(sql.String)
    is_active = sql.Column(sql.Boolean, default=True)
    posts = orm.relationship("Post", back_populates="owner")
    
    
class Post(Base):
    __tablename__ = "posts"
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    title = sql.Column(sql.String, index=True)
    content = sql.Column(sql.String, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    owner = orm.relationship("User", back_populates="posts")
    

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"    
    token = sql.Column(sql.String, primary_key=True, index=True)
