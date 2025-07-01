from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from flask import g

# Global holders for engine and session factory
engine = None
SessionLocal = None

class Base(DeclarativeBase):
    pass


def init_db(app):
    """
    Initialize SQLAlchemy engine and session factory using Flask app config.
    Registers teardown function to close session after each request.
    """
    global engine, SessionLocal

    database_uri = app.config["SQLALCHEMY_DATABASE_URI"]
    pool_size = int(app.config.get("DB_POOL_SIZE", 5))
    max_overflow = int(app.config.get("DB_MAX_OVERFLOW", 10))
    echo = app.config.get("ENV") == "development"

    engine = create_engine(
        database_uri,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_pre_ping=True,
        echo=echo,
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    app.teardown_appcontext(close_db)


def get_db():
    """
    Provide a transactional "scoped" session tied to the Flask 'g' context.
    Creates a new SessionLocal() only if one doesn't already exist in g.

    Returns:
        SQLAlchemy Session object
    """
    if "db" not in g:
        g.db = SessionLocal()
    return g.db


def close_db(e=None):
    """
    Close and remove the database session at the end of the request.

    Args:
        e (Optional[Exception]): Exception, if raised during the request.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


@contextmanager
def transactional_session():
    """
    Provide a transactional scope around a series of operations.
    Commits on success, rolls back on failure.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
