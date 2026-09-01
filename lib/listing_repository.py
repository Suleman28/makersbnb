from lib.listing import Listing


class ListingRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute("SELECT * from listings")
        listings = []
        for row in rows:
            item = Listing(
                row["id"],
                row["name"],
                row["description"],
                row["dates_available"],
                row["price_per_night"],
                row["image_url"],
                row["user_id"],
            )
            listings.append(item)
        return listings

    def find(self, listing_id):
        rows = self._connection.execute(
            "SELECT * from listings WHERE id = %s", [listing_id]
        )
        row = rows[0]
        return Listing(
            row["id"],
            row["name"],
            row["description"],
            row["dates_available"],
            row["price_per_night"],
            row["image_url"],
            row["user_id"],
        )

    def create(self, listing):
        self._connection.execute(
            "INSERT INTO listings (name, description, dates_available, price_per_night, image_url, user_id) VALUES (%s, %s, %s, %s, %s, %s)",
            [
                listing.name,
                listing.description,
                listing.dates_available,
                listing.price_per_night,
                listing.image_url,
                listing.user_id,
            ],
        )
        return None

    def delete(self, listing_id):
        self._connection.execute("DELETE FROM listings WHERE id = %s", [listing_id])
        return None
