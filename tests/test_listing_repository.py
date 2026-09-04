from datetime import date
from decimal import Decimal

from lib.listing import Listing
from lib.listing_repository import ListingRepository
from lib.database_connection import DatabaseConnection


# The seed file is the app's demo data and grows over time, so the list-level
# tests compare identifying fields rather than whole objects - that way adding
# a listing to the seed doesn't require rewriting every expectation here.
def listing_identities(listings):
    return [(listing.id, listing.name, listing.price) for listing in listings]


def test_get_all_listings():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = ListingRepository(connection)

    listings = repo.all()

    assert listing_identities(listings) == [
        (1, "Clifftop Retreat", Decimal("100.99")),
        (2, "Polar Igloo", Decimal("45.99")),
        (3, "Bush Lovers Bothy", Decimal("75.86")),
        (4, "Coastal Retreat & Sunset Haven", Decimal("185.00")),
        (5, "Mountain Lodge", Decimal("245.00")),
        (6, "Downtown Modern Loft", Decimal("160.00")),
        (7, "Desert Oasis Villa", Decimal("290.00")),
        (8, "Lakeside Cabin", Decimal("140.00")),
        (9, "The Treehouse Canopy", Decimal("210.00"))
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
        10
    )

def test_delete_listing():
    connection = DatabaseConnection(test_mode=True)
    connection.connect()
    connection.seed("seeds/seed.sql")
    repo = ListingRepository(connection)

    repo.delete(2)

    listings = repo.all()

    assert listing_identities(listings) == [
        (1, "Clifftop Retreat", Decimal("100.99")),
        (3, "Bush Lovers Bothy", Decimal("75.86")),
        (4, "Coastal Retreat & Sunset Haven", Decimal("185.00")),
        (5, "Mountain Lodge", Decimal("245.00")),
        (6, "Downtown Modern Loft", Decimal("160.00")),
        (7, "Desert Oasis Villa", Decimal("290.00")),
        (8, "Lakeside Cabin", Decimal("140.00")),
        (9, "The Treehouse Canopy", Decimal("210.00"))
    ]
