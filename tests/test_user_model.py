import sys
import os 

from lib.user import User
from lib.booking import Booking
from lib.listing import Listing

#CHANGE USER SEED DATA PASSWORD AS ALL OF THEM ARE THE SAME RIGHT NOW

def testing_user_Peter_details_work_with_default_id():
    user = User("Peter Puffin", "pp@email.com", "12345678")

    assert user.id is None
    assert user.name == "Peter Puffin"
    assert user.email == "pp@email.com"
    assert user.password == "12345678"
    assert repr(user) == "The User's details: (Peter Puffin, pp@email.com)"

def testing_user_Peter_details_are_all_correct_with_id_provided():
    user = User("Peter Puffin", "pp@email.com", "12345678", id = 1)

    assert user.id == 1
    assert user.name == "Peter Puffin"
    assert user.email == "pp@email.com"
    assert user.password == "12345678"
    assert repr(user) == "The User's details: (Peter Puffin, pp@email.com)"

def testing_user_Polly_details_are_all_correct():
    user = User("Polly Penguin", "pollyp@email.com", "12345678", id = 2)

    assert user.id == 2
    assert user.name == "Polly Penguin"
    assert user.email == "pollyp@email.com"
    assert user.password == "12345678"
    assert repr(user) == "The User's details: (Polly Penguin, pollyp@email.com)"

def testing_user_Quentin_details_are_all_correct():
    user = User("Quentin Quail", "qq@email.com", "12345678", id = 3)

    assert user.id == 3
    assert user.name == "Quentin Quail"
    assert user.email == "qq@email.com"
    assert user.password == "12345678"
    assert repr(user) == "The User's details: (Quentin Quail, qq@email.com)"

def test_that_both_users_details_do_not_match():
    user1 = User("Peter Puffin", "pp@email.com", "12345678", id = 1)
    user2 = User("Polly Penguin", "pollyp@email.com", "12345678", id = 2)
    user3 = User("Quentin Quail", "qq@email.com", "12345678", id = 3)

    assert user1 != user2
    assert user2 != user3
    assert user3 != user1


