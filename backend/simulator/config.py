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


_config = load_yaml(path, "config.yaml")

Settings = AppConfig(**_config)
logging.basicConfig(stream=sys.stdout, level=Settings.verbosity, force=True)

def setup_engine(db_url: str = Settings.db_uri):
    set_new_engine(create_engine(url=db_url, echo=False))
