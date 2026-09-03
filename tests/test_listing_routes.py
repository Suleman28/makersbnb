import pytest

SEED_FILE = "seeds/seed.sql"


@pytest.fixture(autouse=True)
def reset_db(db_connection):
    db_connection.seed(SEED_FILE)


def sign_in(web_client, email, password):
    return web_client.post("/sign_in", data={"email": email, "password": password})


def test_get_listings_shows_seeded_listings(web_client):
    response = web_client.get("/listings")
    assert response.status_code == 200
    assert b"Clifftop Retreat" in response.data
    assert b"Polar Igloo" in response.data
    assert b"Bush Lovers Bothy" in response.data


def test_get_single_listing(web_client):
    response = web_client.get("/listings/1")
    assert response.status_code == 200
    assert b"Clifftop Retreat" in response.data
    assert b"A fantastic place for a puffin" in response.data


def test_get_new_listing_page_requires_login(web_client):
    response = web_client.get("/users/3/listings/new")
    assert response.status_code == 302
    assert response.location == "/"


def test_get_new_listing_page_when_signed_in(web_client):
    sign_in(web_client, "qq@email.com", "12649670")  # user id 3
    response = web_client.get("/users/3/listings/new")
    assert response.status_code == 200


def test_get_new_listing_page_rejects_mismatched_user_id(web_client):
    sign_in(web_client, "qq@email.com", "12649670")  # user id 3
    response = web_client.get("/users/2/listings/new")
    assert response.status_code == 302
    assert response.location == "/"


def test_create_listing_success(web_client, db_connection):
    sign_in(web_client, "qq@email.com", "12649670")  # user id 3

    response = web_client.post(
        "/users/3/listings/new",
        data={
            "listing_name": "Seaside Cabin",
            "listing_dates_available": "2027-02-01, 2027-06-01",
            "listing_price": "60.00",
            "listing_image_url": "https://example.com/cabin.jpg",
            "listing_description": "A cosy cabin by the sea.",
        },
    )
    assert response.status_code == 302
    assert response.location == "/listings"

    rows = db_connection.execute(
        "SELECT * FROM listings WHERE name = %s", ["Seaside Cabin"]
    )
    assert len(rows) == 1
    assert rows[0]["user_id"] == 3
    assert str(rows[0]["price"]) == "60.00"


def test_create_listing_requires_login(web_client, db_connection):
    response = web_client.post(
        "/users/3/listings/new",
        data={
            "listing_name": "Unauthorized Cabin",
            "listing_dates_available": "2027-02-01, 2027-06-01",
            "listing_price": "60.00",
            "listing_image_url": "https://example.com/cabin.jpg",
            "listing_description": "Should not be created.",
        },
    )
    assert response.status_code == 302
    assert response.location == "/"

    rows = db_connection.execute(
        "SELECT * FROM listings WHERE name = %s", ["Unauthorized Cabin"]
    )
    assert len(rows) == 0


def test_create_listing_rejects_mismatched_user_id(web_client, db_connection):
    sign_in(web_client, "qq@email.com", "12649670")  # user id 3

    response = web_client.post(
        "/users/2/listings/new",
        data={
            "listing_name": "Impersonated Cabin",
            "listing_dates_available": "2027-02-01, 2027-06-01",
            "listing_price": "60.00",
            "listing_image_url": "https://example.com/cabin.jpg",
            "listing_description": "Should not be created under user 2.",
        },
    )
    assert response.status_code == 302
    assert response.location == "/"

    rows = db_connection.execute(
        "SELECT * FROM listings WHERE name = %s", ["Impersonated Cabin"]
    )
    assert len(rows) == 0
