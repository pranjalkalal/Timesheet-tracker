import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def auth_headers(client: TestClient):
    """Create a test user and return auth headers."""
    # Register user
    client.post(
        "/auth/register",
        json={
            "email": "testuser@example.com",
            "password": "securepassword123"
        }
    )

    # Login to get token
    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "securepassword123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_project(client: TestClient, auth_headers: dict):
    """Test creating a project."""
    response = client.post(
        "/projects",
        headers=auth_headers,
        json={
            "name": "Test Project",
            "description": "A test project"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert "id" in data


def test_list_projects(client: TestClient, auth_headers: dict):
    """Test listing projects."""
    # Create a project
    client.post(
        "/projects",
        headers=auth_headers,
        json={
            "name": "Test Project",
            "description": "A test project"
        }
    )

    # List projects
    response = client.get("/projects", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Project"


def test_create_timesheet(client: TestClient, auth_headers: dict):
    """Test creating a timesheet entry."""
    # Create a project first
    project_response = client.post(
        "/projects",
        headers=auth_headers,
        json={
            "name": "Test Project",
            "description": "A test project"
        }
    )
    project_id = project_response.json()["id"]

    # Create timesheet
    response = client.post(
        "/timesheets",
        headers=auth_headers,
        json={
            "project_id": project_id,
            "date": "2024-01-15",
            "hours": 8.5,
            "note": "Completed feature development"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["hours"] == 8.5
    assert data["date"] == "2024-01-15"
    assert "id" in data


def test_list_timesheets(client: TestClient, auth_headers: dict):
    """Test listing timesheet entries."""
    # Create a project
    project_response = client.post(
        "/projects",
        headers=auth_headers,
        json={
            "name": "Test Project",
            "description": "A test project"
        }
    )
    project_id = project_response.json()["id"]

    # Create a timesheet
    client.post(
        "/timesheets",
        headers=auth_headers,
        json={
            "project_id": project_id,
            "date": "2024-01-15",
            "hours": 8.5,
            "note": "Completed feature development"
        }
    )

    # List timesheets
    response = client.get("/timesheets", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["hours"] == 8.5


def test_update_timesheet(client: TestClient, auth_headers: dict):
    """Test updating a timesheet entry."""
    # Create a project
    project_response = client.post(
        "/projects",
        headers=auth_headers,
        json={
            "name": "Test Project",
            "description": "A test project"
        }
    )
    project_id = project_response.json()["id"]

    # Create a timesheet
    timesheet_response = client.post(
        "/timesheets",
        headers=auth_headers,
        json={
            "project_id": project_id,
            "date": "2024-01-15",
            "hours": 8.5,
            "note": "Completed feature development"
        }
    )
    timesheet_id = timesheet_response.json()["id"]

    # Update timesheet
    response = client.put(
        f"/timesheets/{timesheet_id}",
        headers=auth_headers,
        json={
            "hours": 7.5,
            "note": "Updated note"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["hours"] == 7.5
    assert data["note"] == "Updated note"


def test_delete_timesheet(client: TestClient, auth_headers: dict):
    """Test deleting a timesheet entry."""
    # Create a project
    project_response = client.post(
        "/projects",
        headers=auth_headers,
        json={
            "name": "Test Project",
            "description": "A test project"
        }
    )
    project_id = project_response.json()["id"]

    # Create a timesheet
    timesheet_response = client.post(
        "/timesheets",
        headers=auth_headers,
        json={
            "project_id": project_id,
            "date": "2024-01-15",
            "hours": 8.5,
            "note": "Completed feature development"
        }
    )
    timesheet_id = timesheet_response.json()["id"]

    # Delete timesheet
    response = client.delete(
        f"/timesheets/{timesheet_id}",
        headers=auth_headers
    )
    assert response.status_code == 204

    # Verify deletion
    response = client.get("/timesheets", headers=auth_headers)
    assert len(response.json()) == 0


def test_unauthorized_access(client: TestClient):
    """Test that endpoints require authentication."""
    response = client.get("/projects")
    assert response.status_code == 403
