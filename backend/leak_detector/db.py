from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import config

# SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://sa:Onyks$us@serverdb:1447/NefrytLDSDemo?driver=ODBC+Driver+17+for+SQL+Server'
SQLALCHEMY_DATABASE_URI = \
    'mssql+pyodbc://sa:Onyks$us@serverdb:1447/NefrytLDSDemo' \
    '?driver=ODBC+Driver+18+for+SQL+Server' \
    '&TrustServerCertificate=Yes' \
    '&Encrypt=No' 

engine = create_engine(config.get("db_uri", SQLALCHEMY_DATABASE_URI), echo=False)
Session = sessionmaker(engine)
global_session = Session()
