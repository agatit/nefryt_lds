from .config import config
from sqlalchemy import create_engine


DATABASE_URL = config.get('db_uri')
engine = create_engine(url=DATABASE_URL, echo=False)
