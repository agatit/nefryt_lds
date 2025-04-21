from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import config


DATABASE_URL = config.get('db_uri')
engine = create_engine(url=DATABASE_URL, echo=False)
Session = sessionmaker(engine)
global_session = Session()
