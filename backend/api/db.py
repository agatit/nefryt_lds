from sqlalchemy.orm import Session
from .config import config
from sqlalchemy import create_engine, Engine, MetaData


DATABASE_URL = config.get('db_uri')
engine = create_engine(url=DATABASE_URL, echo=False)
test_engine: Engine


TEST_DATABASE_URL = config.get('test_db_uri')


def get_engine() -> Engine:
    return engine


def get_test_engine() -> Engine:
    return test_engine


def set_test_engine(new_test_engine: Engine):
    global test_engine
    test_engine = new_test_engine


def clear_test_db():
    meta = MetaData()
    meta.reflect(bind=test_engine, schema='editor')
    meta.reflect(bind=test_engine, schema='lds')

    with Session(test_engine) as session:
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()
