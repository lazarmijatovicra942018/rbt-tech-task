import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from flask import g

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')

SQLALCHEMY_DATABASE_URL = \
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=int(os.environ.get('DB_POOL_SIZE', 5)),
    max_overflow=int(os.environ.get('DB_MAX_OVERFLOW', 10)),
    pool_pre_ping=True,
    echo=os.environ.get('ENV') == 'development'
)

# SessionLocal is a factory for new SQLAlchemy sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for declarative SQLAlchemy models
class Base(DeclarativeBase):
    pass


def get_db():
    """
    Provide a transactional "scoped" session tied to the Flask 'g' context.
    Creates a new SessionLocal() only if one doesn't already exist in g.

    Returns:
        SessionLocal instance stored in g.db
    """
    if "db" not in g:
        g.db = SessionLocal()
    return g.db


def close_db(e=None):
    """
    Close and remove the database session at the end of the request.
    This is registered with Flask's teardown_appcontext hook.

    Args:
        exception (Optional[Exception]): the exception that triggered teardown, if any
    """

    db = g.pop("db", None)

    if db is not None:
        db.close()



def init_db(app):
    """
    Initialize database session management for a Flask app.
    Registers teardown_appcontext to ensure sessions are closed.

    This should be called inside your create_app() factory.
    """

    #TODO
    #finish this

    app.teardown_appcontext(close_db)