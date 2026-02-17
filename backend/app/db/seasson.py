from sqlalchemy import create_engine
from app.core.config import settings
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
