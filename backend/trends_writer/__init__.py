# from . import TrendBase
# from . import QuickTrend
# from . import CalcTrend
# from . import MeanTrend
# from . import DerivTrend
# from . import DiffTrend

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://sa:Onyks$us@serverdb:1447/NefrytLDSDemo?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
Session = sessionmaker(engine)
session = Session()