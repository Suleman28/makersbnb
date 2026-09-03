import pytest
from lib.database_connection import DatabaseConnection
from lib.booking_repository import BookingRepository
from app import app

@pytest.fixture
def seeded_db():
  connection = DatabaseConnection(test_mode=True)
  connection.connect()
  connection.seed("seeds/seed.sql")
  return connection

def sign_in_as(web_client, email, password):
  return web_client.post('/sign_in', data={'email': email, 'password': password})

def test_get_host_bookings_requires_login(web_client):
  response = web_client.get('/host/bookings')
  assert response.status_code == 302
  assert response.location == '/'

def test_get_host_bookings_lists_bookings_for_hosts_listings(web_client, seeded_db):
  sign_in_as(web_client, 'qq@email.com', '12649670')

  response = web_client.get('/host/bookings')

  assert response.status_code == 200
  assert b"Clifftop Retreat" in response.data

def test_approve_booking_sets_status_to_booked(web_client, seeded_db):
  sign_in_as(web_client, 'qq@email.com', '12649670')

  response = web_client.post('/host/bookings/1/approve')

  assert response.status_code == 302
  assert response.location == '/host/bookings'
  assert BookingRepository(seeded_db).find(1).status == "BOOKED"

def test_decline_booking_sets_status_to_declined(web_client, seeded_db):
  sign_in_as(web_client, 'qq@email.com', '12649670')

  response = web_client.post('/host/bookings/1/decline')

  assert response.status_code == 302
  assert response.location == '/host/bookings'
  assert BookingRepository(seeded_db).find(1).status == "DECLINED"

def test_cannot_approve_booking_for_another_hosts_listing(web_client, seeded_db):
  sign_in_as(web_client, 'pollyp@email.com', '12345678')

  response = web_client.post('/host/bookings/1/approve')

  assert response.status_code == 302
  assert BookingRepository(seeded_db).find(1).status == "PENDING"
