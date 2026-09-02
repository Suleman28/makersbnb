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
        Booking(date(2027, 1, 5), date(2027, 1, 10), "PENDING", 1, 1),
        Booking(date(2027, 1, 5), date(2027, 1, 12), "PENDING", 2, 2),
        Booking(date(2027, 1, 11), date(2027, 1, 13), "BOOKED", 1, 3),
        Booking(date(2027, 1, 23), date(2027, 1, 25), "BOOKED", 3, 4)
    ]

