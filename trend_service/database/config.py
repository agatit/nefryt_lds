from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.orm import declarative_base
import sqlalchemy
# from sqlalchemy.orm.session import Session
print(__name__)

# mssql+pymssql://sa:Onyks$us@serverdb:1447/NefrytLDSDemo?charset=cp1250
# dialect+driver://username:password@host:port/database?params

DB_USERNAME = 'sa'
DB_PASSWORD = "Onyks$us"
DB_HOST = 'serverdb'
DB_PORT = '1447'
DB_NAME = 'NefrytLDSDemo'
DB_PARAMS = 'charset=cp1250'

"""Setup for the database."""
SQLALCHEMY_DATABASE_URI = f'mssql+pymssql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?{DB_PARAMS}'

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
Base_lds = declarative_base()
Base_lds.metadata.create_all(engine)
Session = sessionmaker(bind=engine, autocommit=True)
Session.configure(bind=engine)
Session = sqlalchemy.orm.Session(bind=engine,future=True)
