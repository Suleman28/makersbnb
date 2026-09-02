from datetime import date
from decimal import Decimal

from lib.listing import Listing
from lib.listing_repository import ListingRepository
from lib.database_connection import DatabaseConnection

def test_get_all_listings():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = ListingRepository(connection)

    listings = repo.all()

    assert listings == [
        Listing(
            "Clifftop Retreat",
            "2027-01-01, 2028-12-12",
            Decimal("100.99"),
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8MC4BiSkd9JxMt3cEdVi4Tj_Xhi9zviXIS4PsGRlPYZMBVnOHMqtPk46D&s=10",
            "A fantastic place for a puffin, or maybe a seagull, great views.",
            3,
            1
        ),
        Listing(
            "Polar Igloo",
            "2027-01-01, 2028-12-12",
            Decimal("45.99"),
            "https://www.lightailing.com/cdn/shop/articles/Polar_Igloo_cover.jpg?v=1568024538",
            "A marvellous joint, if a bit chilly.",
            2,
            2
        ),
        Listing(
            "Bush Lovers Bothy",
            "2027-01-01, 2028-12-12",
            Decimal("75.86"),
            "https://media.newyorker.com/photos/661e7b9dee3bbf86940d41d9/master/w_2560%2Cc_limit/Keeley-Treehouse.jpg",
            "A brilliant abode, get your mud baths in!",
            4,
            3
        )
    ]

def test_find_listing():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = ListingRepository(connection)

    listing = repo.find(2)

    assert listing == Listing(
        "Polar Igloo",
        "2027-01-01, 2028-12-12",
        Decimal("45.99"),
        "https://www.lightailing.com/cdn/shop/articles/Polar_Igloo_cover.jpg?v=1568024538",
        "A marvellous joint, if a bit chilly.",
        2,
        2
    )

def test_create_listing():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = ListingRepository(connection)

    new_listing = Listing(
        "Mountain Cabin",
        "2027-03-01, 2028-12-12",
        Decimal("85.50"),
        "https://example.com/cabin.jpg",
        "A cosy cabin in the mountains.",
        3
    )

    repo.create(new_listing)

    listings = repo.all()

    assert listings[-1] == Listing(
        "Mountain Cabin",
        "2027-03-01, 2028-12-12",
        Decimal("85.50"),
        "https://example.com/cabin.jpg",
        "A cosy cabin in the mountains.",
        3,
        4
    )

def test_delete_listing():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = ListingRepository(connection)

    repo.delete(2)

    listings = repo.all()

    assert listings == [
        Listing(
            "Clifftop Retreat",
            "2027-01-01, 2028-12-12",
            Decimal("100.99"),
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8MC4BiSkd9JxMt3cEdVi4Tj_Xhi9zviXIS4PsGRlPYZMBVnOHMqtPk46D&s=10",
            "A fantastic place for a puffin, or maybe a seagull, great views.",
            3,
            1
        ),
        Listing(
            "Bush Lovers Bothy",
            "2027-01-01, 2028-12-12",
            Decimal("75.86"),
            "https://media.newyorker.com/photos/661e7b9dee3bbf86940d41d9/master/w_2560%2Cc_limit/Keeley-Treehouse.jpg",
            "A brilliant abode, get your mud baths in!",
            4,
            3
        )
    ]