from sqlalchemy.ext import declarative
from sqlalchemy import orm
import sqlalchemy as sql


SQLALCHEMY_URL = "sqlite:///./database.db"

# check same thread alows sqlite to communicate with different threads
engine = sql.create_engine(SQLALCHEMY_URL, connect_args={"check_same_thread": False})

# allows session creation
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for all models
Base = declarative.declarative_base()