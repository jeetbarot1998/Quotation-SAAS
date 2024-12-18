from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from database.dependencies import get_db
from database.session import org_id_ctx
from models.quotation import Quotation, QuotationItem
from models.customer import Customer
from routes.products import get_current_org_id

# Create router
router = APIRouter(
    prefix="/quotations",
    tags=["Quotations"],
    responses={404: {"description": "Not found"}}
)

@router.get(
    "",
    tags=["Quotations"],
    summary="Get quotation details",
    responses={
        200: {
            "description": "Detailed quotation information",
            "content": {
                "application/json": {
                    "example": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "customer": {
                            "id": "customer-uuid",
                            "name": "John Doe",
                            "email": "john@example.com"
                        },
                        "items": [
                            {
                                "product": {
                                    "id": "product-uuid",
                                    "name": "Sample Product",
                                    "price": "29.99"
                                },
                                "quantity": 2,
                                "unit_price": "29.99"
                            }
                        ],
                        "total_amount": "59.98",
                        "created_at": "2024-01-01T00:00:00Z"
                    }
                }
            }
        },
        404: {"description": "Quotation not found"}
    }
)
async def get_quotation(
        quotation_id: str,
        db: Session = Depends(get_db),
        current_org_id: str = Depends(get_current_org_id)
):
    """
    Get detailed quotation information including customer and product details.
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