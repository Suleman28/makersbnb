from lib.database_connection import DatabaseConnection
from lib.booking_repository import BookingRepository
from app import app


def test_get_listing_bookings_lists():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")

    client = app.test_client()

    client.post('/sign_in', data={'email': 'qq@email.com', 'password': '12649670'})

    response = client.get('/listings/1/bookings/1')

    assert response.status_code == 200
    assert b"Clifftop Retreat" in response.data


def test_get_listing_bookings_rejecting_user():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")

    client = app.test_client()

    client.post('/sign_in', data={'email': 'pollyp@email.com', 'password': '12345678'})

    response = client.get('/listings/1/bookings')

    assert response.status_code == 302
    assert response.location == '/'


def test_get_single_booking_rejecting_user():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")

    client = app.test_client()

    client.post('/sign_in', data={'email': 'pollyp@email.com', 'password': '12345678'})

    response = client.get('/listings/1/bookings/1')

    assert response.status_code == 302
    assert response.location == '/'


def test_approve_booking_sets_status_to_booked():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = BookingRepository(connection)

    client = app.test_client()

    client.post('/sign_in', data={'email': 'qq@email.com', 'password': '12649670'})

    response = client.post('/listings/1/bookings/1/approve')

    booking = repo.find(1)

    assert response.status_code == 302
    assert response.location == '/users/3/listings/1/bookings'
    assert booking.status == "BOOKED"


def test_deny_booking_sets_status_to_declined():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = BookingRepository(connection)

    client = app.test_client()

    client.post('/sign_in', data={'email': 'qq@email.com', 'password': '12649670'})

    response = client.post('/listings/1/bookings/1/deny')

    booking = repo.find(1)

    assert response.status_code == 302
    assert response.location == '/users/3/listings/1/bookings'
    assert booking.status == "DECLINED"


def test_cannot_approve_booking_for_another_hosts_listing():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = BookingRepository(connection)

    client = app.test_client()

    client.post('/sign_in', data={'email': 'pollyp@email.com', 'password': '12345678'})

    response = client.post('/listings/1/bookings/1/approve')

    booking = repo.find(1)

    assert response.status_code == 302
    assert booking.status == "PENDING"
