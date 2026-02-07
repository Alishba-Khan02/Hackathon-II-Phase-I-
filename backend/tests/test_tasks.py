from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
import pytest

from backend.src.main import app
from backend.src.database import get_session
from backend.src.models import User, Task
from backend.src.services import tasks as task_service
from backend.src.services.auth import get_password_hash, create_access_token

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

@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    user = User(username="testuser", password_hash=get_password_hash("testpassword"))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture(name="test_auth_token")
def test_auth_token_fixture(test_user: User):
    return create_access_token(data={"sub": test_user.username})

# T018: Backend: Unit tests for task service functions
def test_create_task(session: Session, test_user: User):
    task = task_service.create_task(session, "Test Task", test_user, "Test Description")
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed == False
    assert task.owner_id == test_user.id

def test_get_tasks(session: Session, test_user: User):
    task_service.create_task(session, "Task 1", test_user)
    task_service.create_task(session, "Task 2", test_user)
    tasks = task_service.get_tasks(session, test_user)
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"

def test_get_task(session: Session, test_user: User):
    task = task_service.create_task(session, "Single Task", test_user)
    retrieved_task = task_service.get_task(session, task.id, test_user)
    assert retrieved_task == task

def test_get_task_not_found(session: Session, test_user: User):
    retrieved_task = task_service.get_task(session, 999, test_user)
    assert retrieved_task is None

def test_update_task(session: Session, test_user: User):
    task = task_service.create_task(session, "Old Title", test_user)
    updated_task = task_service.update_task(session, task.id, test_user, title="New Title", completed=True)
    assert updated_task.title == "New Title"
    assert updated_task.completed == True

def test_update_task_not_found(session: Session, test_user: User):
    updated_task = task_service.update_task(session, 999, test_user, title="New Title")
    assert updated_task is None

def test_delete_task(session: Session, test_user: User):
    task = task_service.create_task(session, "Task to Delete", test_user)
    deleted = task_service.delete_task(session, task.id, test_user)
    assert deleted == True
    assert task_service.get_task(session, task.id, test_user) is None

def test_delete_task_not_found(session: Session, test_user: User):
    deleted = task_service.delete_task(session, 999, test_user)
    assert deleted == False

# T019: Backend: Integration tests for all task-related API endpoints
def test_create_task_api(client: TestClient, test_auth_token: str):
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_auth_token}"},
        json={"title": "API Task", "description": "Via API", "completed": False},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "API Task"
    assert "id" in data

def test_get_tasks_api(client: TestClient, session: Session, test_auth_token: str, test_user: User):
    task_service.create_task(session, "API Task 1", test_user)
    task_service.create_task(session, "API Task 2", test_user)
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "API Task 1"
    assert data[1]["title"] == "API Task 2"

def test_get_task_api(client: TestClient, session: Session, test_auth_token: str, test_user: User):
    task = task_service.create_task(session, "API Single Task", test_user)
    response = client.get(
        f"/tasks/{task.id}",
        headers={"Authorization": f"Bearer {test_auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "API Single Task"

def test_get_task_api_not_found(client: TestClient, session: Session, test_auth_token: str, test_user: User):
    # Ensure there are no tasks for the user initially
    assert len(task_service.get_tasks(session, test_user)) == 0
    
    response = client.get(
        "/tasks/999",
        headers={"Authorization": f"Bearer {test_auth_token}"},
    )
    assert response.status_code == 404

def test_update_task_api(client: TestClient, session: Session, test_auth_token: str, test_user: User):
    task = task_service.create_task(session, "API Old Title", test_user)
    response = client.put(
        f"/tasks/{task.id}",
        headers={"Authorization": f"Bearer {test_auth_token}"},
        json={"title": "API New Title", "description": "New Desc", "completed": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "API New Title"
    assert data["completed"] == True

def test_delete_task_api(client: TestClient, session: Session, test_auth_token: str, test_user: User):
    task = task_service.create_task(session, "API Task to Delete", test_user)
    response = client.delete(
        f"/tasks/{task.id}",
        headers={"Authorization": f"Bearer {test_auth_token}"},
    )
    assert response.status_code == 204
    assert task_service.get_task(session, task.id, test_user) is None

def test_complete_task_api(client: TestClient, session: Session, test_auth_token: str, test_user: User):
    task = task_service.create_task(session, "API Task to Complete", test_user, completed=False)
    response = client.patch(
        f"/tasks/{task.id}/complete",
        headers={"Authorization": f"Bearer {test_auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] == True

def test_uncomplete_task_api(client: TestClient, session: Session, test_auth_token: str, test_user: User):
    task = task_service.create_task(session, "API Task to Uncomplete", test_user, completed=True)
    response = client.patch(
        f"/tasks/{task.id}/uncomplete",
        headers={"Authorization": f"Bearer {test_auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] == False
