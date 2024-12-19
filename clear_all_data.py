from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Import your models
from models import Base, QuotationItem, Quotation, Product, Customer, User, Organization

# Database configuration
DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def clear_all_data():
    db = SessionLocal()
    try:
        # Disable foreign key checks temporarily
        db.execute(text("SET CONSTRAINTS ALL DEFERRED"))

        # Clear tables in reverse order of dependencies
        tables = [
            QuotationItem,
            Quotation,
            Product,
            Customer,
            User,
            Organization
        ]

        for table in tables:
            print(f"Clearing table: {table.__tablename__}")
            db.query(table).delete()

        # Re-enable foreign key checks
        db.execute(text("SET CONSTRAINTS ALL IMMEDIATE"))

        # Commit the changes
        db.commit()
        print("Successfully cleared all data from the database!")

    except Exception as e:
        db.rollback()
        print(f"Error clearing data: {e}")
        raise
    finally:
        db.close()


def reset_sequences():
    """Reset all auto-increment sequences to 1"""
    db = SessionLocal()
    try:
        # Get all sequences
        sequences_query = text("""
            SELECT sequence_name 
            FROM information_schema.sequences 
            WHERE sequence_schema = 'public'
        """)

        sequences = db.execute(sequences_query).fetchall()

        # Reset each sequence
        for seq in sequences:
            print(f"Resetting sequence: {seq[0]}")
            db.execute(text(f"ALTER SEQUENCE {seq[0]} RESTART WITH 1"))

        db.commit()
        print("Successfully reset all sequences!")

    except Exception as e:
        db.rollback()
        print(f"Error resetting sequences: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting database cleanup...")
    clear_all_data()
    reset_sequences()
    print("Database cleanup completed!")