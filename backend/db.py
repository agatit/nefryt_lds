from sqlalchemy import Engine


_engine: Engine | None = None

def set_new_engine(new_engine: Engine):
    global _engine
    _engine = new_engine


def get_engine() -> Engine:
    assert _engine is not None
    return _engine
