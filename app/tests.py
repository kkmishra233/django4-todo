import uuid
import json
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from app.models import Todo

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_password():
   return 'strong-test-pass'

@pytest.fixture
def create_user(db, django_user_model, test_password):
   def make_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       return django_user_model.objects.create_user(**kwargs)
   return make_user

@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
   def make_auto_login(user=None):
       if user is None:
           user = create_user()
       client.login(username=user.username, password=test_password)
       return client, user
   return make_auto_login

@pytest.fixture
def create_todo(create_user):
    def _create_todo(owner=None):
        if not owner:
            owner = create_user()
        return Todo.objects.create(task="Sample task", description="Task should be completed by John Doe", owner=owner)
    return _create_todo

@pytest.mark.django_db
def test_create_todo(auto_login_user):
    client, user = auto_login_user()
    url = reverse("todo-list")
    data = {"task": "Sample task", "description": "A task for Author Name", "owner": user}
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.data["task"] == "Sample task"

@pytest.mark.django_db
def test_get_todo(auto_login_user, create_todo):
    client, user = auto_login_user()
    create_todo(owner=user)
    url = reverse("todo-list")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) > 0

@pytest.mark.django_db
def test_update_todo(auto_login_user, create_todo):
    client, user = auto_login_user()
    todo = create_todo(owner=user)
    url = reverse("todo-detail", args=[todo.id])
    data = {"task": "Updated task", "description": todo.description}
    response = client.put(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    assert response.data["task"] == "Updated task"

@pytest.mark.django_db
def test_delete_todo(auto_login_user, create_todo):
    client, user = auto_login_user()
    todo = create_todo(owner=user)
    url = reverse("todo-detail", args=[todo.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert not Todo.objects.filter(id=todo.id).exists()
