import os
import types

import flask_sqlalchemy
import sqlalchemy as sql
from sqlalchemy.orm import declarative_base

from .models import lds, editor

db = flask_sqlalchemy.SQLAlchemy()

SPEC_DIR = os.path.dirname(__file__)
SPEC_FILE = os.path.join(SPEC_DIR, "openapi\openapi.yaml")

def columns_to_dict(self):
    dict_ = {}
    for key in self.__mapper__.c.keys():
        dict_[key] = getattr(self, key)
    return dict_

# modele są generowane, więc uzupełniam metodę columns_to_dict w runtime
lds.Base.columns_to_dict = columns_to_dict
editor.Base.columns_to_dict = columns_to_dict