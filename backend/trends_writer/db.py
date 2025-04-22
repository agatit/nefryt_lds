from sqlalchemy import create_engine, MetaData, Engine
from sqlalchemy.orm import Session
from .config import config


DATABASE_URL = config.get('db_uri')
_engine = create_engine(url=DATABASE_URL, echo=False)


def set_new_engine(new_engine: Engine):
    global _engine
    _engine = new_engine


def get_engine() -> Engine:
    return _engine


def clear_test_db():
    meta = MetaData()
    meta.reflect(bind=_engine, schema='editor')
    meta.reflect(bind=_engine, schema='lds')

    with Session(_engine) as session:
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()
