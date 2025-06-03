from typing import Type
from sqlmodel import SQLModel


def to_dict(o) -> dict:
    return {c.name: getattr(o, c.name) for c in o.__table__.columns}


def strip_strings_in_dict(d: dict) -> dict:
    return {k: v.strip() if isinstance(v, str) else v for k, v in d.items()}


def strip_strings(obj: SQLModel | Type[SQLModel]):
    for name, value in obj.__dict__.items():
        if isinstance(value, str):
            setattr(obj, name, value.strip())
    return obj
