from fastapi import FastAPI

from database.session import SessionLocal
from middleware.tenant import TenantMiddleware

app = FastAPI()

# Add tenant middleware
app.add_middleware(TenantMiddleware, db_session=SessionLocal())