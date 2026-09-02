from lib.booking import Booking
from lib.booking_repository import BookingRepository
from lib.database_connection import DatabaseConnection
from datetime import date

def test_get_all_bookings():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = BookingRepository(connection)

    bookings = repo.all()

    assert bookings == [
        Booking(date(2027, 1, 5), "2027-01-10", "PENDING", 2, 1),
        Booking("2027-01-05", "2027-01-10", "PENDING", 3, 2),
        Booking("2027-01-11", "2027-01-13", "BOOKED", 3, 3)
    ]

