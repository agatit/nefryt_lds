import os
import sys
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, Connection
from sqlalchemy.orm import Session
from testcontainers.mssql import SqlServerContainer

from trends_writer.trend.base import TrendBaseMeta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # noqa: E402
from trends_writer.db import clear_test_db, set_new_engine, get_engine
from database.models.lds import Base as ldsBase
from database.models.editor import Base as editorBase
from trends_writer.config import config


TEST_DATABASE_URI = str()
TEST_DATABASE_NAME = str()
SERVER_URL = str()


def prepare_test_db_data():
    global TEST_DATABASE_URI, TEST_DATABASE_NAME, SERVER_URL
    if not os.path.exists(".env"):
        raise FileNotFoundError("Need .env file with TEST_DB_PASSWORD environment variable defined to run tests")
    load_dotenv()
    test_db_password = os.getenv("TEST_DB_PASSWORD")
    if not test_db_password:
        raise ValueError("Need TEST_DB_PASSWORD environment variable defined to run tests")
    TEST_DATABASE_URI = config.get("test_db_uri").format(test_db_password=test_db_password)
    TEST_DATABASE_NAME = config.get('test_db_name')
    SERVER_URL = config.get('server_url_for_tests').format(test_db_password=test_db_password)


def drop_database(conn: Connection):
    conn.execute(text("USE master"))
    conn.execute(text(f"ALTER DATABASE {TEST_DATABASE_NAME} SET SINGLE_USER WITH ROLLBACK IMMEDIATE"))
    conn.execute(text(f"DROP DATABASE {TEST_DATABASE_NAME}"))


@pytest.fixture(scope="session", autouse=True)
def setup_test_database(request):
    db_type = request.config.db_type
    if db_type == 'temp':
        prepare_test_db_data()
        engine = create_engine(SERVER_URL)
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM sys.databases WHERE name = '{TEST_DATABASE_NAME}'"))
            db_exists = result.scalar() > 0
            if db_exists:
                drop_database(conn)

            conn.execute(text(f"CREATE DATABASE {TEST_DATABASE_NAME}"))
            conn.execute(text(f"USE {TEST_DATABASE_NAME}"))
            conn.execute(text("CREATE SCHEMA lds"))
            conn.execute(text("CREATE SCHEMA editor"))

        engine.dispose()

        test_engine = create_engine(url=TEST_DATABASE_URI, echo=False)
        ldsBase.metadata.create_all(bind=test_engine)
        editorBase.metadata.create_all(bind=test_engine)
        set_new_engine(test_engine)

        yield

        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            drop_database(conn)

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

            set_new_engine(test_engine)

            yield


@pytest_asyncio.fixture(scope="function")
async def reset_lds_objects(request):
    return request.param()


@pytest_asyncio.fixture(scope="function")
async def add_lds_objects(reset_lds_objects):
    lds_objects = reset_lds_objects
    with Session(get_engine()) as session:
        for lds_objects_list in lds_objects:
            print(lds_objects_list)
            session.add_all(lds_objects_list)
            session.commit()
        for lds_object in (obj for sublist in lds_objects for obj in sublist):
            session.refresh(lds_object)


@pytest.fixture(autouse=True)
def reset_db_status():
    clear_test_db()


@pytest.fixture(autouse=True)
def set_log_level(caplog):
    caplog.set_level("WARNING")


@pytest.fixture(scope="session", autouse=True)
def disable_cache():
    TrendBaseMeta.use_cache = False
