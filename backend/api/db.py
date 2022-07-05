from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import flask_sqlalchemy

from .config import config
from .app import app

# SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://sa:Onyks$us@serverdb:1447/NefrytLDSDemo?driver=ODBC+Driver+17+for+SQL+Server'
SQLALCHEMY_DATABASE_URI = \
    'mssql+pyodbc://sa:Onyks$us@serverdb:1447/NefrytLDSDemo' \
    '?driver=ODBC+Driver+18+for+SQL+Server' \
    '&TrustServerCertificate=Yes' \
    '&Encrypt=No' 


app.app.config['SQLALCHEMY_DATABASE_URI'] = config.get("db_uri", SQLALCHEMY_DATABASE_URI)
db = flask_sqlalchemy.SQLAlchemy()
db.init_app(app.app)

session = db.session