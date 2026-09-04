from datetime import date

from lib.booking import Booking
from lib.booking_repository import BookingRepository
from lib.database_connection import DatabaseConnection


def test_get_all_bookings():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = BookingRepository(connection)

    bookings = repo.all()

    assert bookings == [
        Booking(date(2027, 1, 5), date(2027, 1, 10), "PENDING", 1, 2, 1),
        Booking(date(2027, 1, 5), date(2027, 1, 12), "PENDING", 2, 3, 2),
        Booking(date(2027, 1, 11), date(2027, 1, 13), "BOOKED", 1, 4, 3),
        Booking(date(2027, 1, 23), date(2027, 1, 25), "BOOKED", 3, 1, 4)
    ]

def test_find_booking():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = BookingRepository(connection)

    booking = repo.find(2)

    assert booking == Booking(date(2027, 1, 5), date(2027, 1, 12), "PENDING", 2, 3, 2)

def test_create_booking():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = BookingRepository(connection)

    booking = Booking(date(2027, 2, 1), date(2027, 2, 5), "PENDING", 1, 2)

    repo.create(booking)

    bookings = repo.all()

    assert bookings[-1] == Booking(date(2027, 2, 1), date(2027, 2, 5), "PENDING", 1, 2, 5)

def test_delete_booking():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = BookingRepository(connection)

    repo.delete(2)

    bookings = repo.all()

    assert bookings == [
        Booking(date(2027, 1, 5), date(2027, 1, 10), "PENDING", 1, 2, 1),
        Booking(date(2027, 1, 11), date(2027, 1, 13), "BOOKED", 1, 4, 3),
        Booking(date(2027, 1, 23), date(2027, 1, 25), "BOOKED", 3, 1, 4)
    ]

def test_update_booking_status_managed_by_host():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = BookingRepository(connection)

    repo.update_booking_status_managed_by_host(2, "DECLINED")

    booking = repo.find(2)

    assert booking == Booking(date(2027, 1, 5), date(2027, 1, 12), "DECLINED", 2, 3, 2)

def test_find_all_listings_booked():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = BookingRepository(connection)

    bookings = repo.find_all_listings(1)

    assert bookings == [
        Booking(date(2027, 1, 5), date(2027, 1, 10), "PENDING", 1, 2, 1),
        Booking(date(2027, 1, 11), date(2027, 1, 13), "BOOKED", 1, 4, 3)
    ]