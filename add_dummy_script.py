from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal

from configs.db_config import settings
from models.organization import Organization
from models.customer import Customer
from models.product import Product
from models.quotation import Quotation, QuotationItem
from auth.security import get_password_hash
from models.user import User

# Create database engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()


def create_dummy_data():
    try:
        # Create an organization
        org = Organization(
            name="Acme Corp",
            subdomain="acme"
        )
        db.add(org)
        db.flush()

        print(f"Created organization: {org.name} with ID: {org.id}")

        # Create admin and regular users
        admin_user = User(
            email="admin@acme.com",
            hashed_password=get_password_hash("Asdfghjkl@123"),
            full_name="Admin User",
            role="admin",
            org_id=org.id
        )

        regular_user = User(
            email="user@acme.com",
            hashed_password=get_password_hash("Asdfghjkl@123"),
            full_name="Regular User",
            role="user",
            org_id=org.id
        )

        db.add(admin_user)
        db.add(regular_user)
        db.flush()

        print(f"Created admin user: {admin_user.email}")
        print(f"Created regular user: {regular_user.email}")

        # Create a customer
        customer = Customer(
            name="John Doe",
            email="john.doe@example.com",
            org_id=org.id
        )
        db.add(customer)
        db.flush()
        print(f"Created customer: {customer.name} with ID: {customer.id}")

        # Create some products with image URLs
        products = [
            Product(
                name="Laptop",
                price=Decimal("999.99"),
                sku="LAP-001",
                image_url="https://support.rebrandly.com/hc/article_attachments/17527840087837",
                org_id=org.id
            ),
            Product(
                name="Mouse",
                price=Decimal("29.99"),
                sku="MOU-001",
                image_url="https://support.rebrandly.com/hc/article_attachments/17527840087837",
                org_id=org.id
            ),
            Product(
                name="Keyboard",
                price=Decimal("59.99"),
                sku="KEY-001",
                image_url="https://support.rebrandly.com/hc/article_attachments/17527840087837",
                org_id=org.id
            )
        ]

        for product in products:
            db.add(product)
        db.flush()
        print(f"Created {len(products)} products")

        # Create a quotation
        quotation = Quotation(
            quote_number=f"Q-2024-{org.id:04d}-001",
            customer_id=customer.id,
            total_amount=Decimal("1089.97"),
            org_id=org.id
        )
        db.add(quotation)
        db.flush()

        # Create quotation items
        quotation_items = [
            QuotationItem(
                quotation_id=quotation.id,
                product_id=products[0].id,
                quantity=1,
                unit_price=products[0].price,
                org_id=org.id
            ),
            QuotationItem(
                quotation_id=quotation.id,
                product_id=products[1].id,
                quantity=1,
                unit_price=products[1].price,
                org_id=org.id
            ),
            QuotationItem(
                quotation_id=quotation.id,
                product_id=products[2].id,
                quantity=1,
                unit_price=products[2].price,
                org_id=org.id
            )
        ]

        for item in quotation_items:
            db.add(item)

        print(f"Created quotation {quotation.quote_number} with {len(quotation_items)} items")

        # Commit all changes
        db.commit()
        print("All data committed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_dummy_data()