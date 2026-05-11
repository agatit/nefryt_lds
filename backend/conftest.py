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
from config import Config, Settings, env_file_path, setup_engine
from config_utils import load_yaml, clear_test_db
from db import set_new_engine, get_engine
from trends_writer.config import TrendsWriterSettings

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
path = pathlib.Path(__file__).parent.resolve()


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
    Config.tests = True
    db_type = request.config.db_type
    if db_type == 'temp':
        engine = create_engine(Settings.TEST_DB_MASTER_URI)
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM sys.databases WHERE name = '{Settings.TEST_DB_DB}'"))
            db_exists = result.scalar() > 0
            if db_exists:
                drop_database(conn, Settings.TEST_DB_DB)

            conn.execute(text(f"CREATE DATABASE {Settings.TEST_DB_DB}"))
            conn.execute(text(f"USE {Settings.TEST_DB_DB}"))
            conn.execute(text("CREATE SCHEMA lds"))
            conn.execute(text("CREATE SCHEMA editor"))

        engine.dispose()

        test_engine = create_engine(url=Settings.TEST_DB_URI, echo=False)
        SQLModel.metadata.create_all(test_engine)
        create_procedure(test_engine)
        set_new_engine(test_engine)

        yield

        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            drop_database(conn, Settings.TEST_DB_DB)

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


@pytest.fixture(autouse=True)
def reset_db_status():
    clear_test_db()


@pytest.fixture(autouse=True)
def set_log_level(caplog):
    caplog.set_level("WARNING")
