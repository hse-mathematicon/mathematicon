from sqlalchemy import event
from sqlalchemy.engine import Engine, create_engine

from app.settings.db import DBSettings


def get_engine(db_settings: DBSettings) -> Engine:
    engine = create_engine(url=db_settings.url)

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):  # type: ignore
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine
