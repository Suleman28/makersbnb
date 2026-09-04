from lib.database_connection import DatabaseConnection
from lib.booking_repository import BookingRepository


# These tests use the `web_client` fixture rather than app.test_client() directly:
# the fixture sets app.config['TESTING'], which is what makes the app talk to the
# test database. Without it the app writes to the development database.


def test_get_listing_bookings_lists(web_client):
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")

    web_client.post('/sign_in', data={'email': 'qq@email.com', 'password': '12649670'})

    response = web_client.get('/listings/1/bookings/1')

    assert response.status_code == 200
    assert b"Clifftop Retreat" in response.data


def test_get_listing_bookings_rejecting_user(web_client):
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")

    web_client.post('/sign_in', data={'email': 'pollyp@email.com', 'password': '12345678'})

    response = web_client.get('/users/3/listings/1/bookings')

    assert response.status_code == 302
    assert response.location == '/'


def test_get_single_booking_rejecting_user(web_client):
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")

    web_client.post('/sign_in', data={'email': 'pollyp@email.com', 'password': '12345678'})

    response = web_client.get('/listings/1/bookings/1')

    assert response.status_code == 302
    assert response.location == '/'


def test_approve_booking_sets_status_to_booked(web_client):
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = BookingRepository(connection)

    web_client.post('/sign_in', data={'email': 'qq@email.com', 'password': '12649670'})

    response = web_client.post('/listings/1/bookings/1/approve')

    booking = repo.find(1)

    assert response.status_code == 302
    assert response.location == '/users/3/listings/1/bookings'
    assert booking.status == "BOOKED"


def test_deny_booking_sets_status_to_declined(web_client):
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = BookingRepository(connection)

    web_client.post('/sign_in', data={'email': 'qq@email.com', 'password': '12649670'})

    response = web_client.post('/listings/1/bookings/1/deny')

    booking = repo.find(1)

    assert response.status_code == 302
    assert response.location == '/users/3/listings/1/bookings'
    assert booking.status == "DECLINED"


def test_cannot_approve_booking_for_another_hosts_listing(web_client):
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = BookingRepository(connection)

    web_client.post('/sign_in', data={'email': 'pollyp@email.com', 'password': '12345678'})

    response = web_client.post('/listings/1/bookings/1/approve')

    booking = repo.find(1)

    assert response.status_code == 302
    assert booking.status == "PENDING"
