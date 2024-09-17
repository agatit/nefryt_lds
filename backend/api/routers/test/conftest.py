import os
import sys
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from testcontainers.mssql import SqlServerContainer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.config import config
from api.db import clear_test_db, set_test_engine, get_test_engine
from database.models.lds import Base as ldsBase
from database.models.editor import Base as editorBase


TEST_DATABASE_URL = config.get('test_db_uri')
TEST_DATABASE_NAME = config.get('test_db_name')
SERVER_URL = config.get('server_url_for_tests')


# creates new db for testing purposes and drops it after all tests if db_type is 'temp'
@pytest.fixture(scope="session", autouse=True)
def setup_test_database(request):
    db_type = request.config.db_type
    if db_type == 'temp':
        engine = create_engine(SERVER_URL)
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM sys.databases WHERE name = '{TEST_DATABASE_NAME}'"))
            db_exists = result.scalar() > 0

            if not db_exists:
                conn.execute(text(f"CREATE DATABASE {TEST_DATABASE_NAME}"))
                conn.execute(text(f"USE {TEST_DATABASE_NAME}"))
                conn.execute(text("CREATE SCHEMA lds"))
                conn.execute(text("CREATE SCHEMA editor"))

        engine.dispose()

        test_engine = create_engine(url=TEST_DATABASE_URL, echo=False)
        ldsBase.metadata.create_all(bind=test_engine)
        editorBase.metadata.create_all(bind=test_engine)
        set_test_engine(test_engine)

        yield

        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            conn.execute(text("USE master"))
            conn.execute(text(f"ALTER DATABASE {TEST_DATABASE_NAME} SET SINGLE_USER WITH ROLLBACK IMMEDIATE"))
            conn.execute(text(f"DROP DATABASE {TEST_DATABASE_NAME}"))

        engine.dispose()
    elif db_type == 'tc':
        with SqlServerContainer() as mssql:
            test_engine_url = mssql.get_connection_url()

            test_engine = create_engine(test_engine_url, echo=False)

            with test_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
                conn.execute(text("CREATE SCHEMA lds"))
                conn.execute(text("CREATE SCHEMA editor"))

            ldsBase.metadata.create_all(bind=test_engine)
            editorBase.metadata.create_all(bind=test_engine)

            set_test_engine(test_engine)

            yield


# has to reset objects manually because of session.refresh() which happens inside of add_lds_objects
@pytest.fixture(scope="function")
def reset_lds_objects(request):
    return request.param()


@pytest.fixture(scope="function")
def add_lds_objects(reset_lds_objects):
    lds_objects = reset_lds_objects
    with Session(get_test_engine()) as session:
        for lds_objects_list in lds_objects:
            session.add_all(lds_objects_list)
            session.commit()
        for lds_object in (obj for sublist in lds_objects for obj in sublist):
            session.refresh(lds_object)


@pytest.fixture(autouse=True)
def reset_db_status():
    clear_test_db()
