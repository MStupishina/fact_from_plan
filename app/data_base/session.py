from sqlalchemy import create_engine
from dotenv import dotenv_values
from sqlalchemy.orm import sessionmaker

from app.data_base.models import Base

config = dotenv_values(".env")

engine = create_engine(config['DATA_BASE_URL'], echo=True)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)