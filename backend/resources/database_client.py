from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from config.environmentConfig import settings
from utilities.logger import logger

DATABASE_URL = settings.database_url
MODE = settings.mode

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)
Base = declarative_base()

try:
    if MODE == "ci" or MODE == "testing":
        logger.info("Skipping database connection")
    else:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connected successfully")

except Exception as e:
    logger.error(f"Database connection failed: {e}")
    raise


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
