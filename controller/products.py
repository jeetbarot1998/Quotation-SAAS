from main import app
import uuid
from fastapi import HTTPException, Depends, Request
from typing import List
from sqlalchemy.orm import Session, joinedload
from database.dependencies import get_db
from database.session import org_id_ctx
from models.product import Product ,ProductResponse, ProductCreate
from models.quotation import Quotation, QuotationItem
from models.customer import Customer

async def get_current_org_id(request: Request) -> str:
    return request.state.org_id


@app.get("/api/products", response_model=List[ProductResponse])
async def list_products(
        db: Session = Depends(get_db),
        current_org_id: str = Depends(get_current_org_id)
):
    """
    List products - automatically filtered by organization
    """
    # Set org_id in context
    org_id_ctx.set(current_org_id)

    # Query will automatically include org_id filter
    products = db.query(Product).all()
    return products


@app.post("/api/products")
async def create_product(
        product_data: ProductCreate,
        db: Session = Depends(get_db),
        current_org_id: str = Depends(get_current_org_id)
):
    """
    Create product - automatically associated with organization
    """
    product = Product(
        id=str(uuid.uuid4()),
        name=product_data.name,
        price=product_data.price,
        sku=product_data.sku,
        org_id=current_org_id  # Automatically set organization
    )

    db.add(product)
    db.commit()
    return product


# Example of complex queries with relationships
@app.get("/api/quotations/{quotation_id}")
async def get_quotation(
        quotation_id: str,
        db: Session = Depends(get_db),
        current_org_id: str = Depends(get_current_org_id)
):
    """
    Get quotation with related data - all automatically org-scoped
    """
    org_id_ctx.set(current_org_id)

    quotation = db.query(Quotation) \
        .join(Customer) \
        .options(
        joinedload(Quotation.customer),
        joinedload(Quotation.items).joinedload(QuotationItem.product)
    ) \
        .filter(Quotation.id == quotation_id) \
        .first()

    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    return quotation