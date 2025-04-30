import os
from pathlib import Path
import yaml
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from db import get_engine


def load_yaml(path: Path, filename: str) -> dict:
    with open(os.path.join(path, filename)) as f:
        config = yaml.safe_load(f)
    return config if config is not None else {}


def clear_test_db():
    meta = MetaData()
    engine = get_engine()
    meta.reflect(bind=engine, schema='editor')
    meta.reflect(bind=engine, schema='lds')

    with Session(engine) as session:
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()
