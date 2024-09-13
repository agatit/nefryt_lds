from sqlalchemy.orm import Session
from .config import config
from sqlalchemy import create_engine, Engine, MetaData
from database.models.lds import Base as ldsBase
from database.models.editor import Base as editorBase


DATABASE_URL = config.get('db_uri')
engine = create_engine(url=DATABASE_URL, echo=False)


TEST_DATABASE_URL = config.get('test_db_uri')
test_engine = create_engine(url=TEST_DATABASE_URL, echo=False)
ldsBase.metadata.create_all(bind=test_engine)
editorBase.metadata.create_all(bind=test_engine)


def get_engine() -> Engine:
    return engine


def get_test_engine() -> Engine:
    return test_engine


def clear_test_db():
    global test_engine
    meta = MetaData()
    meta.reflect(bind=test_engine, schema='editor')
    meta.reflect(bind=test_engine, schema='lds')

    with Session(test_engine) as session:
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()
