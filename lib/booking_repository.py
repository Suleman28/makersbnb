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

    # Check whether a listing has an overlapping confirmed booking
    def is_available(self, listing_id, start_date, end_date):
        rows = self._connection.execute(
            '''
            SELECT id FROM bookings
            WHERE listing_id = %s
              AND status = 'BOOKED'
              AND start_date < %s
              AND end_date > %s
            LIMIT 1
            ''',
            [listing_id, end_date, start_date])
        return len(rows) == 0

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
