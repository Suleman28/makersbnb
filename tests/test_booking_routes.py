import pytest

SEED_FILE = "seeds/seed.sql"


@pytest.fixture(autouse=True)
def reset_db(db_connection):
    db_connection.seed(SEED_FILE)


def sign_in(web_client, email, password):
    return web_client.post("/sign_in", data={"email": email, "password": password})


def test_create_booking_requires_login(web_client, db_connection):
    response = web_client.post(
        "/bookings",
        data={
            "listing_id": "1",
            "start_date": "2027-02-01",
            "end_date": "2027-02-05",
        },
    )
    assert response.status_code == 302
    assert response.location == "/sign_in"

    rows = db_connection.execute(
        "SELECT * FROM bookings WHERE start_date = %s AND end_date = %s",
        ["2027-02-01", "2027-02-05"],
    )
    assert len(rows) == 0


def test_create_booking_success(web_client, db_connection):
    sign_in(web_client, "pp@email.com", "12445778")  # user id 1

    response = web_client.post(
        "/bookings",
        data={
            "listing_id": "1",
            "start_date": "2027-02-01",
            "end_date": "2027-02-05",
        },
    )
    assert response.status_code == 302
    assert response.location == "/listings/1"

    rows = db_connection.execute(
        "SELECT * FROM bookings WHERE start_date = %s AND end_date = %s AND listing_id = %s",
        ["2027-02-01", "2027-02-05", 1],
    )
    assert len(rows) == 1
    assert rows[0]["status"] == "PENDING"


def test_create_booking_rejects_overlapping_dates(web_client, db_connection):
    sign_in(web_client, "pp@email.com", "12445778")  # user id 1

    # Listing 1 already has a PENDING booking for 2027-01-05 to 2027-01-10
    response = web_client.post(
        "/bookings",
        data={
            "listing_id": "1",
            "start_date": "2027-01-06",
            "end_date": "2027-01-08",
        },
    )
    assert response.status_code == 302
    assert response.location == "/listings/1"

    rows = db_connection.execute(
        "SELECT * FROM bookings WHERE start_date = %s AND end_date = %s AND listing_id = %s",
        ["2027-01-06", "2027-01-08", 1],
    )
    assert len(rows) == 0


def test_get_travel_bookings_requires_login(web_client):
    response = web_client.get("/users/1/bookings")
    assert response.status_code == 302
    assert response.location == "/"


def test_get_travel_bookings_when_signed_in(web_client):
    sign_in(web_client, "pp@email.com", "12445778")  # user id 1
    response = web_client.get("/users/1/bookings")
    assert response.status_code == 200
