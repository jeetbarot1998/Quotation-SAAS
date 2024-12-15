from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from database.session import org_id_ctx
from models.organization import Organization

class TenantMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, db_session: Session):
        super().__init__(app)
        self.db = db_session

    async def dispatch(self, request: Request, call_next):
        # Get host from request headers
        host = request.headers.get('host', '')
        subdomain = self.get_subdomain(host)

        if not subdomain:
            raise HTTPException(status_code=400, detail="Invalid subdomain")

        # Get organization by subdomain
        org = self.db.query(Organization).filter_by(subdomain=subdomain).first()
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        # Set org_id in context
        org_id_ctx.set(org.id)

        response = await call_next(request)
        return response

    def get_subdomain(self, host: str):
        try:
            # Handle localhost
            if 'localhost' in host:
                host = host.split(':')[0]
                parts = host.split('.')
                return parts[0] if len(parts) > 2 else None

            # Handle production domain
            parts = host.split('.')
            if len(parts) > 2:
                return parts[0]

            return None

        except Exception:
            return None