

from sqlalchemy import create_engine, alias, select, delete, and_, lambda_stmt
from sqlalchemy.orm import Session

from database.models import lds


SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://@localhost/NefrytLDS_Zygmuntow_2022?driver=ODBC+Driver+17+for+SQL+Server'

if __name__ == '__main__':
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    with Session(engine) as session:
        stmt = select([lds.TrendData]).order_by(lds.TrendData.Time.desc()).limit(1)
        db_trend_data = session.execute(stmt)
        latest = next(db_trend_data)
        print(latest[0].Time)