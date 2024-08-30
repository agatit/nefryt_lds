from .config import config
from sqlalchemy import create_engine

# SQLALCHEMY_DATABASE_URI = \
#     'mssql+pyodbc://sa:Onyks$us@serverdb:1447/NefrytLDSDemo' \
#     '?driver=ODBC+Driver+18+for+SQL+Server' \
#     '&TrustServerCertificate=Yes' \
#     '&Encrypt=No'

DATABASE_URL = config.get('db_uri')


# app.app.config['SQLALCHEMY_DATABASE_URI'] = config.get("db_uri", SQLALCHEMY_DATABASE_URI)
engine = create_engine(url=DATABASE_URL, echo=False)
