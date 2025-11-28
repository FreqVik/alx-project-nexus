from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings


Base = declarative_base()
Engine = create_engine(settings.database_url, connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {})
Session_Local = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

def create_tables():
    Base.metadata.create_all(bind=Engine)

def get_db():
    db=Session_Local()
    try:
        yield db
    finally:
        db.close()
