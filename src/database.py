import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '1999')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'real_estate_db')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', "localhost")

SQLALCHEMY_DATABASE_URL = \
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=int(os.environ.get('DB_POOL_SIZE',5)),
    max_overflow=int(os.environ.get('DB_MAX_OVERFLOW', 10)),
    pool_pre_ping=True,
    echo=os.environ.get('ENV') == 'development'
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()