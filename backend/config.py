import sys
import pathlib
import logging
from pydantic import BaseModel
from sqlalchemy import create_engine
from config_utils import load_yaml
from db import set_new_engine

path = pathlib.Path(__file__).parent.resolve()


class AppConfig(BaseModel):
    db_uri: str
    verbosity: str = 'INFO'
    tests: bool = False
    trends_writer: dict
    simulator: dict


app_config = load_yaml(path, "config.yaml")
Settings = AppConfig(**app_config)
logging.basicConfig(stream=sys.stdout, level=Settings.verbosity, force=True)


def setup_engine(db_uri: str | None = None):
    db_url = db_uri if db_uri else Settings.db_uri
    set_new_engine(create_engine(url=db_url, echo=False))
