from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    import models.availability  # noqa: F401
    import models.booking  # noqa: F401
    import models.user  # noqa: F401

    Base.metadata.create_all(bind=engine)
