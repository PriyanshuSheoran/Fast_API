import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app  
from app.database import get_db
from app.models import Base


TEST_DATABASE_URL = "mysql+pymysql://test_user:test_password@localhost/test_db"


engine = create_engine(TEST_DATABASE_URL)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create the test database tables before running tests."""
    Base.metadata.create_all(bind=engine) 
    yield  
    Base.metadata.drop_all(bind=engine)  


@pytest.fixture(scope="function")
def db():
    """Provide a clean database session for each test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()  
        session.close()


@pytest.fixture(scope="function")
def client(db):
    """Create a FastAPI test client using the overridden test database."""
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db  
    return TestClient(app)
