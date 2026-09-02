from random import seed

import pytest
from lib.database_connection import DatabaseConnection
from lib.user_repository import UserRepository
from app import app

@pytest.fixture
def seeded_db():
  connection = DatabaseConnection(test_mode=True)
  connection.connect()
  connection.seed("seeds/seed.sql")
  return connection

def test_get_signup_renders_form(web_client):
  response = web_client.get('/sign_up')
  assert response.status_code == 200

def test_get_signin_renders_form(web_client):
  response = web_client.get('/sign_in')
  assert response.status_code == 200

def test_signup_with_valid_data_creates_user_and_sets_session(web_client, seeded_db):
  response = web_client.post('/sign_up', data={
    'name': 'John Doe',
    'email': 'john.doe@example.com',
    'password': 'abcdefgh@12',
    'password_confirmation': 'abcdefgh@12'
  })

  assert response.status_code == 302
  assert response.location == '/'

  with web_client.session_transaction() as sess:
    assert sess['user_id'] is not None

  created_user = UserRepository(seeded_db).find_by_email('john.doe@example.com')
  assert created_user is not None

def test_signup_with_mismatched_passwords_return_400_and_creates_no_user(web_client, seeded_db):
  response = web_client.post('/sign_up', data={
    'name': 'John Doe',
    'email': 'john.doe@example.com',
    'password': 'abcdefgh@12',
    'password_confirmation': 'differentPassword'
  })

  assert response.status_code == 400
  assert b"Passwords do not match" in response.data

  created_user = UserRepository(seeded_db).find_by_email('john.doe@example.com')
  assert created_user is None

def test_signin_with_correct_credentials_redirects_and_sets_session(web_client, seeded_db):
  response = web_client.post('/sign_in', data={
    'email': 'pp@email.com',
    'password': '12445778'
  })

  assert response.status_code == 302
  assert response.location == '/'

  with web_client.session_transaction() as sess:
    assert sess['user_id'] is not None

def test_signin_with_wrong_password_returns_401(web_client, seeded_db):
  response = web_client.post('/sign_in', data={
    'email': 'pp@email.com',
    'password': 'wrongpassword123'
  })

  assert response.status_code == 401
  assert b"invalid email or password" in response.data

def test_signin_with_unknown_email_returns_401(web_client, seeded_db):
  response = web_client.post('/sign_in', data={
    'email': 'john.nobody@example.com',
    'password': 'nobody'
  })

  assert response.status_code == 401
  assert b"invalid email or password" in response.data

def test_sign_out_clears_session(web_client, seeded_db):
  web_client.post('/sign_in', data={
    'email': 'pp@email.com',
    'password': '12445778'
  })

  response = web_client.post('/sign_out')

  assert response.status_code == 302
  assert response.location == '/'

  with web_client.session_transaction() as sess:
    assert 'user_id' not in sess

def test_sign_out_with_get_is_not_allowed(web_client):
  response = web_client.get('/sign_out')
  assert response.status_code == 405
