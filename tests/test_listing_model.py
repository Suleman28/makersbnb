import sys
import os 

from lib.listing import Listing

def testing_clifftop_retreat_seed_listing_works():
    listing = Listing(
        'Clifftop Retreat',
        '2027-01-01, 2028-12-12',
        100.99,
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8MC4BiSkd9JxMt3cEdVi4Tj_Xhi9zviXIS4PsGRlPYZMBVnOHMqtPk46D&s=10',
        'A fantastic place for a puffin, or maybe a seagull, great views.',
        3,
        id=1
    )

    assert listing.id == 1
    assert listing.name == 'Clifftop Retreat'
    assert listing.dates_available == '2027-01-01, 2028-12-12'
    assert listing.price == 100.99
    assert listing.image_url == 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8MC4BiSkd9JxMt3cEdVi4Tj_Xhi9zviXIS4PsGRlPYZMBVnOHMqtPk46D&s=10'
    assert listing.description == 'A fantastic place for a puffin, or maybe a seagull, great views.'
    assert listing.user_id == 3

def testing_polar_igloo_seed_listing_works():
    listing = Listing(
        'Polar Igloo',
        '2027-01-01, 2028-12-12',
        45.99,
        'https://www.lightailing.com/cdn/shop/articles/Polar_Igloo_cover.jpg?v=1568024538',
        'A marvellous joint, if a bit chilly.',
        2,
        id=2
    )

    assert listing.id == 2
    assert listing.name == 'Polar Igloo'
    assert listing.dates_available == '2027-01-01, 2028-12-12'
    assert listing.price == 45.99
    assert listing.image_url == 'https://www.lightailing.com/cdn/shop/articles/Polar_Igloo_cover.jpg?v=1568024538'
    assert listing.description == 'A marvellous joint, if a bit chilly.'
    assert listing.user_id == 2

def testing_bush_lovers_bothy_seed_listing_works():
    listing = Listing(
        'Bush Lovers Bothy',
        '2027-01-01, 2028-12-12',
        75.86,
        'https://media.newyorker.com/photos/661e7b9dee3bbf86940d41d9/master/w_2560%2Cc_limit/Keeley-Treehouse.jpg',
        'A brilliant abode, get your mud baths in!',
        4,
        id=3
    )

    assert listing.id == 3
    assert listing.name == 'Bush Lovers Bothy'
    assert listing.dates_available == '2027-01-01, 2028-12-12'
    assert listing.price == 75.86
    assert listing.image_url == 'https://media.newyorker.com/photos/661e7b9dee3bbf86940d41d9/master/w_2560%2Cc_limit/Keeley-Treehouse.jpg'
    assert listing.description == 'A brilliant abode, get your mud baths in!'
    assert listing.user_id == 4

def testing_seed_listings_are_not_equal():
    listing1 = Listing(
        'Clifftop Retreat',
        '2027-01-01, 2028-12-12',
        100.99,
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8MC4BiSkd9JxMt3cEdVi4Tj_Xhi9zviXIS4PsGRlPYZMBVnOHMqtPk46D&s=10',
        'A fantastic place for a puffin, or maybe a seagull, great views.',
        3,
        id=1
    )
    listing2 = Listing(
        'Polar Igloo',
        '2027-01-01, 2028-12-12',
        45.99,
        'https://www.lightailing.com/cdn/shop/articles/Polar_Igloo_cover.jpg?v=1568024538',
        'A marvellous joint, if a bit chilly.',
        2,
        id=2
    )
    listing3 = Listing(
        'Bush Lovers Bothy',
        '2027-01-01, 2028-12-12',
        75.86,
        'https://media.newyorker.com/photos/661e7b9dee3bbf86940d41d9/master/w_2560%2Cc_limit/Keeley-Treehouse.jpg',
        'A brilliant abode, get your mud baths in!',
        4,
        id=3
    )

    assert listing1 != listing2
    assert listing3 != listing1