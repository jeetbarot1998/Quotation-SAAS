# reset_db.py
from sqlalchemy import create_engine, text
import alembic.config

from configs.db_config import settings


def reset_database():
    # Connect to database
    engine = create_engine(settings.DATABASE_URL)

    with engine.connect() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
        connection.commit()

    # Run all alembic migrations
    alembic_cfg = alembic.config.Config("alembic.ini")
    alembic.command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    reset_database()