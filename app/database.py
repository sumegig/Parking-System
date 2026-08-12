from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

#database engine
engine = create_engine(settings.DATABASE_URL)

#session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#base class for SQLalcemy models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()