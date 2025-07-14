from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace with your actual database URL
DATABASE_URL = "sqlite:///./product.db"  # or "postgresql://user:password@localhost/dbname"

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # `connect_args` is needed for SQLite only

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()