import pytest
from flask import session


SEED_FILE = "seeds/seed.sql"


@pytest.fixture(autouse=True)
def reset_db(db_connection):
    db_connection.seed(SEED_FILE)


def test_get_signup_page(web_client):
    response = web_client.get("/sign_up")
    assert response.status_code == 200
    assert b"Sign up" in response.data


def test_create_account_success(web_client, db_connection):
    response = web_client.post(
        "/sign_up",
        data={
            "name": "New User",
            "email": "newuser@email.com",
            "password": "password123",
            "password_confirmation": "password123",
        },
    )
    assert response.status_code == 302
    assert response.location == "/"

    rows = db_connection.execute(
        "SELECT * FROM users WHERE email = %s", ["newuser@email.com"]
    )
    assert len(rows) == 1
    assert rows[0]["name"] == "New User"


def test_create_account_sets_session(web_client):
    web_client.post(
        "/sign_up",
        data={
            "name": "Session User",
            "email": "sessionuser@email.com",
            "password": "password123",
            "password_confirmation": "password123",
        },
    )
    assert session["user_id"] is not None


def test_create_account_password_mismatch(web_client, db_connection):
    response = web_client.post(
        "/sign_up",
        data={
            "name": "Bad User",
            "email": "baduser@email.com",
            "password": "password123",
            "password_confirmation": "differentpassword",
        },
    )
    assert response.status_code == 400
    assert b"Passwords do not match" in response.data

    rows = db_connection.execute(
        "SELECT * FROM users WHERE email = %s", ["baduser@email.com"]
    )
    assert len(rows) == 0


def test_get_signin_page(web_client):
    response = web_client.get("/sign_in")
    assert response.status_code == 200


def test_sign_in_success(web_client):
    response = web_client.post(
        "/sign_in",
        data={"email": "pp@email.com", "password": "12445778"},
    )
    assert response.status_code == 302
    assert response.location == "/"


def test_sign_in_sets_session(web_client):
    web_client.post(
        "/sign_in",
        data={"email": "pp@email.com", "password": "12445778"},
    )
    assert session["user_id"] == 1


def test_sign_in_wrong_password(web_client):
    response = web_client.post(
        "/sign_in",
        data={"email": "pp@email.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert b"invalid email or password" in response.data


def test_sign_in_unknown_email(web_client):
    response = web_client.post(
        "/sign_in",
        data={"email": "doesnotexist@email.com", "password": "whatever"},
    )
    assert response.status_code == 401


def test_sign_out_clears_session(web_client):
    web_client.post(
        "/sign_in",
        data={"email": "pp@email.com", "password": "12445778"},
    )
    response = web_client.post("/sign_out")
    assert response.status_code == 302
    assert response.location == "/"
    assert "user_id" not in session


def test_index_shows_current_user_when_signed_in(web_client):
    web_client.post(
        "/sign_in",
        data={"email": "pp@email.com", "password": "12445778"},
    )
    response = web_client.get("/")
    assert response.status_code == 200
    assert b"Peter Puffin" in response.data
