import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# Use an in-memory SQLite database for testing purposes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Creates a fresh database schema for each test,
    yielding the session, and drops it afterwards.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    
    # Insert a dummy parking space for the tests
    from app.models.parking_space import ParkingSpace
    test_space = ParkingSpace(id=1, code="TEST-101", type="REGULAR", is_active=True)
    session.add(test_space)
    session.commit()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Overrides the get_db dependency to use the test database
    and returns the FastAPI TestClient.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()