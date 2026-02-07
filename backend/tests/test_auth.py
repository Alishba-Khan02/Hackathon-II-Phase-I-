from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
import pytest

from backend.src.main import app
from backend.src.database import get_session
from backend.src.models import User
from backend.src.services.auth import get_password_hash, verify_password, create_access_token

# Setup a test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

# Override get_session dependency for tests
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

# T010: Backend: Unit tests for user creation and password hashing
def test_get_password_hash():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != password

def test_verify_password():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)
    assert not verify_password("wrongpassword", hashed_password)

# T011: Backend: Integration tests for /signup and /login endpoints
def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={"username": "testuser", "password_hash": "testpassword"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password_hash" in data # This will be the hashed password
    assert data["password_hash"] != "testpassword" # Ensure it's hashed

def test_login_for_access_token(client: TestClient):
    # First, create a user
    client.post(
        "/users/",
        json={"username": "testuser", "password_hash": "testpassword"},
    )
    
    # Then, attempt to login
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    data = response.json()

    assert response.status_code == 200
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_for_access_token_invalid_credentials(client: TestClient):
    response = client.post(
        "/token",
        data={"username": "nonexistent", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
