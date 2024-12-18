from fastapi import FastAPI
from database.session import SessionLocal
from middleware.tenant import TenantMiddleware
from fastapi.middleware.cors import CORSMiddleware
import routes.products as products
import routes.quotation as quotation
import routes.organization as org

app = FastAPI(
    title="Multi-tenant Product Management API",
    description="""
    A REST API for managing products and quotations in a multi-tenant environment.
    Each organization (tenant) has its own isolated data accessed via subdomains.
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "jeetbarot1998@gmail.com",
    },
    license_info={
        "name": "MIT",
    }
)

# Add middleware
app.add_middleware(TenantMiddleware, db_session=SessionLocal())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes
app.include_router(products.router, prefix="/api")
app.include_router(quotation.router, prefix="/api")
app.include_router(org.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)