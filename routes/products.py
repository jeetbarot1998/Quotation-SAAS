from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
import uuid

from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from auth.security import verify_token
from database.dependencies import get_db
from database.session import org_id_ctx
from schemas.product import ProductResponse, ProductCreate
from models import Product
from schemas.user import TokenData
from utils.validate_org_domain import validate_org_domain

# Create router
router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Not found"}}
)

security = HTTPBearer()

async def get_current_org_id(request: Request) -> str:
    """
    Dependency to get current organization ID from request state.
    """
    return request.state.org_id


@router.get(
    "",
    response_model=List[ProductResponse],
    tags=["Products"],
    summary="List all products",
    response_description="List of products for the current organization"
)
@validate_org_domain()
async def list_products(
        request: Request,
        db: Session = Depends(get_db),
        token_data: TokenData = Depends(verify_token),
        current_org_id: str = Depends(get_current_org_id)
):
    """
    Retrieve all products for the current organization.
    """
    org_id_ctx.set(current_org_id)
    products = db.query(Product).all()
    return products


@router.post(
    "",
    response_model=ProductResponse,
    tags=["Products"],
    summary="Create a new product",
    status_code=201,
    responses={
        201: {
            "description": "Product created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "New Product",
                        "price": "99.99",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z"
                    }
                }
            }
        },
        400: {"description": "Invalid input"},
        401: {"description": "Authentication required"},
        403: {"description": "Invalid organization or insufficient permissions"}
    }
)
@validate_org_domain()
async def create_product(
        product_data: ProductCreate,
        db: Session = Depends(get_db),
        current_org_id: str = Depends(get_current_org_id)
):
    """
    Create a new product for the current organization.
    """
    product = Product(
        id=str(uuid.uuid4()),
        name=product_data.name,
        price=product_data.price,
        sku=product_data.sku,
        org_id=current_org_id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product