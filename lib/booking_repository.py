from lib.booking import Booking 

class BookingRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all bookings
    def all(self):
        rows = self._connection.execute('SELECT * from bookings')
        bookings = []
        for row in rows:
            item = Booking(row["start_date"], row["end_date"], row["status"], row["listing_id"], row["id"])
            bookings.append(item)
        return bookings

    # Find a single booking by its id
    def find(self, booking_id):
        rows = self._connection.execute(
            'SELECT * from bookings WHERE id = %s', [booking_id])
        row = rows[0]
        return Booking(row["start_date"], row["end_date"], row["status"], row["listing_id"], row["id"])

    # Create a new booking
    def create(self, booking):
        self._connection.execute('INSERT INTO bookings (start_date, end_date, status, listing_id) VALUES (%s, %s, %s, %s)', [
                                booking.start_date, booking.end_date, booking.status, booking.listing_id])
        return None

    # Delete a booking by its id
    def delete(self, booking_id):
        self._connection.execute(
            'DELETE FROM bookings WHERE id = %s', [booking_id])
        return None
