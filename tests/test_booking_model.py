import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.booking import Booking


def testing_first_line_of_seed_booking():
    booking = Booking("2027-01-05", "2027-01-10", "PENDING", 1, id= 1)

    assert booking.id == 1
    assert booking.start_date ==  "2027-01-05"
    assert booking.end_date == "2027-01-10"
    assert booking.status == "PENDING"
    assert booking.listing_id == 1
    assert repr(booking) == "The Booking details: (1, PENDING, 2027-01-05_2027-01-10)"

def testing_second_line_of_seed_booking():
    booking = Booking("2027-01-05", "2027-01-12", "PENDING", 2, id= 2)

    assert booking.id == 2
    assert booking.start_date ==  "2027-01-05"
    assert booking.end_date == "2027-01-12"
    assert booking.status == "PENDING"
    assert booking.listing_id == 2
    assert repr(booking) == "The Booking details: (2, PENDING, 2027-01-05_2027-01-12)"

def testing_third_line_of_seed_booking():
    booking = Booking("2027-01-11", "2027-01-13", "BOOKED", 1, id= 3)

    assert booking.id == 3
    assert booking.start_date ==  "2027-01-11"
    assert booking.end_date == "2027-01-13"
    assert booking.status == "PENDING"
    assert booking.listing_id == 1
    assert repr(booking) == "The Booking details: (1, BOOKED, 2027-01-11_2027-01-13)"

def testing_fourth_line_of_seed_booking():
    booking = Booking("2027-01-23", "2027-01-25", "BOOKED", 3, id= 4)

    assert booking.id == 4
    assert booking.start_date ==  "2027-01-23"
    assert booking.end_date == "2027-01-25"
    assert booking.status == "BOOKED"
    assert booking.listing_id == 3
    assert repr(booking) == "The Booking details: (3, BOOKED, 2027-01-23_2027-01-25)"

def testing_seed_booking_data_are_not_equal():
    booking1 = Booking("2027-01-05", "2027-01-10", "PENDING", 1, id= 1)
    booking2 = Booking("2027-01-05", "2027-01-12", "PENDING", 2, id= 2)
    booking3 = Booking("2027-01-11", "2027-01-13", "BOOKED", 1, id= 3)
    booking4 = Booking("2027-01-23", "2027-01-25", "BOOKED", 3, id= 4)

    assert booking1 != booking2
    assert booking2 != booking3
    assert booking3 != booking4
    assert booking4 != booking1

def testing_bookings_with_same_listing_id_are_not_equal():
    booking1 = Booking("2027-01-05", "2027-01-10", "PENDING", 1, id= 1)
    booking3 = Booking("2027-01-11", "2027-01-13", "BOOKED", 1, id= 3)

    assert booking1.listing_id == booking3.listing_id

def test_booking_with_empty_strings():
    booking = Booking("", "", "", "")

    assert booking.id is None
    assert booking.start_date == ""
    assert booking.end_date == ""
    assert booking.status == ""
    assert booking.listing_id == ""
