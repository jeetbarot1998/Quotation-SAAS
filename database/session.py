from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextvars import ContextVar
from models.base import TenantAwareModel
from configs.db_config import settings

# Create engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Context variable to store current org_id
org_id_ctx = ContextVar("org_id", default=None)


class TenantAwareSession(Session):
    """
    Custom session class that automatically filters queries by org_id
    """

    def query(self, *args, **kwargs):
        query = super().query(*args, **kwargs)

        # Get the first entity being queried
        entity = args[0] if args else None

        # If entity is tenant-aware, automatically filter by org_id
        if entity and issubclass(entity, TenantAwareModel):
            org_id = org_id_ctx.get()
            if org_id:
                query = query.filter(entity.org_id == org_id)

        return query