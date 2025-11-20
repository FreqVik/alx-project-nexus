from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


db_url="sqlite:///./polls.db"

Base = declarative_base()
Engine = create_engine(db_url, connect_args={"check_same_thread": False})
Session_Local = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

def create_tables():
    Base.metadata.create_all()

def get_db():
    db=Session_Local()
    try:
        yield db
    finally:
        db.close()