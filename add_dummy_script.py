from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal
from datetime import datetime, timedelta
import uuid

# Import your models here
from models import Base, Organization, User, Customer, Product, Quotation, QuotationItem

# Database configuration
DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def create_dummy_data():
    db = SessionLocal()
    try:
        # Create organizations
        orgs = [
            Organization(
                name="TechCorp Solutions",
                subdomain="techcorp",
                description="Enterprise Technology Solutions",
                email="contact@techcorp.com"
            ),
            Organization(
                name="Digital Dynamics",
                subdomain="digidyn",
                description="Digital Transformation Services",
                email="info@digidyn.com"
            )
        ]

        for org in orgs:
            db.add(org)
        db.flush()

        # Create users for each organization
        for org in orgs:
            users = [
                User(
                    email=f"admin@{org.subdomain}.com",
                    hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKxcQw8.1w5ExKa",
                    # Password: Admin123!
                    full_name="Admin User",
                    role="admin",
                    org_id=org.id,
                ),
                User(
                    email=f"sales@{org.subdomain}.com",
                    hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKxcQw8.1w5ExKa",
                    # Password: Admin123!
                    full_name="Sales Manager",
                    role="sales",
                    org_id=org.id,
                )
            ]

            for user in users:
                db.add(user)
            db.flush()

            # Create customers for each organization
            customers = [
                Customer(
                    name="John Smith",
                    email="john.smith@example.com",
                    phone="+1-555-0123",
                    address="123 Business Ave, Suite 100, New York, NY 10001",
                    org_id=org.id
                ),
                Customer(
                    name="Sarah Johnson",
                    email="sarah.j@example.com",
                    phone="+1-555-0124",
                    address="456 Tech Street, San Francisco, CA 94105",
                    org_id=org.id
                )
            ]

            for customer in customers:
                db.add(customer)
            db.flush()

            # Create products for each organization
            products = [
                Product(
                    name="Enterprise Server X1",
                    description="High-performance enterprise server",
                    sku="SRV-001",
                    price=Decimal("5999.99"),
                    stock_quantity=10,
                    org_id=org.id
                ),
                Product(
                    name="Cloud Security Suite",
                    description="Complete cloud security solution",
                    sku="CSS-001",
                    price=Decimal("1999.99"),
                    stock_quantity=50,
                    org_id=org.id
                ),
                Product(
                    name="AI Analytics Platform",
                    description="Enterprise AI analytics solution",
                    sku="AI-001",
                    price=Decimal("3999.99"),
                    stock_quantity=20,
                    org_id=org.id
                )
            ]

            for product in products:
                db.add(product)
            db.flush()

            # Create quotations for each customer
            for customer in customers:
                quotation = Quotation(
                    quote_number=f"Q-{datetime.now().year}-{org.id:04d}-{customer.id:04d}",
                    customer_id=customer.id,
                    total_amount=Decimal("11999.97"),
                    validity_period=datetime.utcnow() + timedelta(days=30),
                    shipping_address=customer.address,
                    tax_amount=Decimal("960.00"),
                    discount_amount=Decimal("500.00"),
                    payment_terms="Net 30",
                    installation_required=True,
                    reference_number=f"REF-{datetime.now().year}-{customer.id:04d}",
                    sales_rep_id=users[1].id,  # Sales manager
                    notes="Enterprise deployment package",
                    sla_terms="99.99% uptime guaranteed",
                    warranty_info="3-year enterprise warranty",
                    compliance_certificates="ISO 27001, SOC 2",
                    environmental_impact="Energy Star certified",
                    technical_support_details="24/7 dedicated support",
                    status="draft",
                    org_id=org.id
                )

                db.add(quotation)
                db.flush()

                # Create quotation items
                for i, product in enumerate(products):
                    item = QuotationItem(
                        quotation_id=quotation.id,
                        product_id=product.id,
                        quantity=1,
                        unit_price=product.price,
                        discount_percent=Decimal("5.00"),
                        notes=f"Enterprise license included",
                        org_id=org.id
                    )
                    db.add(item)

                db.flush()

        # Commit all changes
        db.commit()
        print("Successfully created dummy data!")

    except Exception as e:
        db.rollback()
        print(f"Error creating dummy data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_dummy_data()