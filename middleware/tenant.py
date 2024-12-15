from idlelib.query import Query

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from database.session import org_id_ctx
from models.organization import Organization
from utils.debug_query import debug_query  # Import the decorator function


class TenantMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, db_session: Session):
        super().__init__(app)
        self.db = db_session
        # Define paths that don't require tenant validation
        self.public_paths = {
            "/docs",  # Swagger UI
            "/redoc",  # ReDoc UI
            "/openapi.json",  # OpenAPI schemas
            "/api/quotation/organizations/"
        }

    @debug_query
    def get_organization(self, subdomain: str) -> Query:
        return self.db.query(Organization).filter_by(subdomain=subdomain)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Allow access to Swagger documentation without tenant validation
        if path in self.public_paths or path.startswith("/static/") or path.startswith("/docs/"):
            return await call_next(request)

        print("========== inside middle ware with path : " + str(path))

        # Get host from request headers
        host = request.headers.get('host', '')
        subdomain = self.get_subdomain(host)

        if not subdomain:
            raise HTTPException(status_code=400, detail="Invalid subdomain")

        # Get organization by subdomain
        org = self.get_organization(subdomain).first()

        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        # Set org_id in context
        org_id_ctx.set(org.id)
        request.state.org_id = org.id  # Store org_id in request state for easy access

        response = await call_next(request)
        return response

    def get_subdomain(self, host: str):
        try:
            # Handle localhost
            if 'localhost' in host:
                host = host.split(':')[0]
                parts = host.split('.')
                if parts[0] == 'localhost':
                    return 'default'  # Use 'default' for localhost without subdomain
                return parts[0] if len(parts) > 2 else None

            # Handle production domain
            parts = host.split('.')
            if len(parts) > 2:
                return parts[0]
            elif len(parts) == 2:
                return 'default'  # Use 'default' for main domain without subdomain

            return None

        except Exception:
            return None