from lib.database_connection import DatabaseConnection
from lib.booking_repository import BookingRepository
from app import app

def sign_in_as(web_client, email, password):
    return web_client.post('/sign_in', data={'email': email, 'password': password})

def test_get_listing_bookings_requiring_a_login(web_client):
    response = web_client.get('/users/3/listings/1/bookings')
    assert response.status_code == 302
    assert response.location == '/'

def test_get_listing_bookings_lists(web_client):
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")

    sign_in_as(web_client, 'qq@email.com', '12649670')

    response = web_client.get('/users/3/listings/1/bookings')

    assert response.status_code == 200
    assert b"Clifftop Retreat" in response.data

def test_get_listing_bookings_rejecting_user(web_client):
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")

    sign_in_as(web_client, 'pollyp@email.com', '12345678')

    response = web_client.get('/users/3/listings/1/bookings')

    assert response.status_code == 302
    assert response.location == '/'

def test_get_single_booking_requiring_login(web_client):
    response = web_client.get('/listings/1/bookings/1')
    assert response.status_code == 302
    assert response.location == '/'

def test_get_single_booking_shows_the_booking(web_client):
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")

    sign_in_as(web_client, 'qq@email.com', '12649670')

    response = web_client.get('/listings/1/bookings/1')

    assert response.status_code == 200
    assert b"Clifftop Retreat" in response.data

def test_get_single_booking_rejecting_user(web_client):
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")

    sign_in_as(web_client, 'pollyp@email.com', '12345678')

    response = web_client.get('/listings/1/bookings/1')

    assert response.status_code == 302
    assert response.location == '/'

def test_approve_booking_sets_status_to_booked(web_client):
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")

    sign_in_as(web_client, 'qq@email.com', '12649670')

    response = web_client.post('/listings/1/bookings/1/approve')

    assert response.status_code == 302
    assert response.location == '/users/3/listings/1/bookings'
    assert BookingRepository(connection).find(1).status == "BOOKED"

def test_deny_booking_sets_status_to_declined(web_client):
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")

    sign_in_as(web_client, 'qq@email.com', '12649670')

    response = web_client.post('/listings/1/bookings/1/deny')

    assert response.status_code == 302
    assert response.location == '/users/3/listings/1/bookings'
    assert BookingRepository(connection).find(1).status == "DECLINED"

def test_cannot_approve_booking_for_another_hosts_listing(web_client):
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")

    sign_in_as(web_client, 'pollyp@email.com', '12345678')

    response = web_client.post('/listings/1/bookings/1/approve')

    assert response.status_code == 302
    assert BookingRepository(connection).find(1).status == "PENDING"
