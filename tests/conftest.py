import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.session import get_db

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set up the database with the tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    """
    A dependency override for tests to use the in-memory database.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the app's dependency with the test one
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    """
    A fixture that provides a TestClient for making requests to the app.
    It also handles creating and tearing down the database tables for each test function.
    """
    Base.metadata.create_all(bind=engine) # Create tables
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine) # Drop tables
