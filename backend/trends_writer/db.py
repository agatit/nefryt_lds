from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://sa:Onyks$us@serverdb:1447/NefrytLDSDemo?driver=ODBC+Driver+17+for+SQL+Server'
# SQLALCHEMY_DATABASE_URI = \
#     'mssql+pyodbc://sa:Onyks$us@serverdb:1447/NefrytLDSDemo' \
#     '?driver=ODBC+Driver+18+for+SQL+Server' \
#     '&TrustServerCertificate=Yes' \
#     '&Encrypt=No' 


engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
Session = sessionmaker(engine)
session = Session()