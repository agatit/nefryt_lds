import multiprocessing
import os
import pathlib
import sys
import pytest
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, text, Connection, Engine
from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from testcontainers.mssql import SqlServerContainer
from config import Settings
from config_utils import load_yaml, clear_test_db
from db import set_new_engine, get_engine
from trends_writer.config import TrendsWriterSettings

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
path = pathlib.Path(__file__).parent.resolve()


class PasswordSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(path, '.env'), env_file_encoding='utf-8')
    password_test: str = Field(alias='PASSWORD_TEST_DB')


class TestModel(BaseModel):
    db_uri: str
    server_url: str
    db_name: str = 'NefrytLDS_Test_Database'


class TestConfig(BaseModel):
    test_model: TestModel
    password_settings: PasswordSettings


_config_test = load_yaml(path, "config.test.yaml")
TestSettings = TestConfig(test_model=TestModel(**_config_test), password_settings=PasswordSettings()) # type: ignore
TrendsWriterSettings.log_profiler = False

def pytest_addoption(parser):
    parser.addoption(
        "--db",
        action="store",
        default="temp",
        help="Type of database to use. Options are: 'temp' (temporary), 'tc' (testcontainers). Default is 'temp'."
    )


def pytest_configure(config):
    db_type = config.getoption("db")
    if db_type not in ["temp", "tc"]:
        raise ValueError(f"Unsupported database type: {db_type}")
    config.db_type = db_type


def drop_database(conn: Connection, test_db_name: str):
    conn.execute(text("USE master"))
    conn.execute(text(f"ALTER DATABASE {test_db_name} SET SINGLE_USER WITH ROLLBACK IMMEDIATE"))
    conn.execute(text(f"DROP DATABASE {test_db_name}"))


def create_procedure(engine: Engine):
    with Session(engine) as session:
        session.execute(text("""
            CREATE PROCEDURE Update_Insert_TrendData
                @trend_id INT,
                @time BIGINT,
                @value BINARY(200)
                AS
                    BEGIN
                        UPDATE lds.TrendData
                        SET Data = @value
                        WHERE TrendID = @trend_id AND Time = @time;
                    
                        IF @@ROWCOUNT = 0
                        BEGIN
                            INSERT INTO lds.TrendData (TrendID, Time, Data)
                            VALUES (@trend_id, @time, @value);
                        END
                    END
                """))
        session.commit()


def cleanup_processes_after_tests():
    for p in multiprocessing.active_children():
        p.terminate()
        p.join(timeout=5)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database(request):
    db_type = request.config.db_type
    test_db_uri = TestSettings.test_model.db_uri.format(db_password=TestSettings.password_settings.password_test)
    test_db_name = TestSettings.test_model.db_name
    server_url = TestSettings.test_model.server_url.format(db_password=TestSettings.password_settings.password_test)
    Settings.db_uri = test_db_uri
    if db_type == 'temp':
        engine = create_engine(server_url)
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM sys.databases WHERE name = '{test_db_name}'"))
            db_exists = result.scalar() > 0
            if db_exists:
                drop_database(conn, test_db_name)

            conn.execute(text(f"CREATE DATABASE {test_db_name}"))
            conn.execute(text(f"USE {test_db_name}"))
            conn.execute(text("CREATE SCHEMA lds"))
            conn.execute(text("CREATE SCHEMA editor"))

        engine.dispose()

        test_engine = create_engine(url=test_db_uri, echo=False)
        SQLModel.metadata.create_all(test_engine)
        create_procedure(test_engine)
        set_new_engine(test_engine)

        yield

        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            drop_database(conn, test_db_name)

        engine.dispose()
    elif db_type == 'tc':
        with SqlServerContainer() as mssql:
            test_engine_url = mssql.get_connection_url()

            test_engine = create_engine(test_engine_url, echo=False)

            with test_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
                conn.execute(text("CREATE SCHEMA lds"))
                conn.execute(text("CREATE SCHEMA editor"))

            SQLModel.metadata.create_all(test_engine)
            create_procedure(test_engine)
            set_new_engine(test_engine)

            yield

    cleanup_processes_after_tests()

@pytest.fixture(scope="function")
def reset_lds_objects(request):
    return request.param()


@pytest.fixture(scope="function")
def add_lds_objects(reset_lds_objects):
    lds_objects = reset_lds_objects
    with Session(get_engine()) as session:
        for lds_objects_list in lds_objects:
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
