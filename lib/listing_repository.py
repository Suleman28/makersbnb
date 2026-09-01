from lib.listing import Listing


class ListingRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute("SELECT * from listings")
        listings = []
        for row in rows:
            item = Listing(
                row["name"],
                row["dates_available"],
                row["price"],
                row["image_url"],
                row["description"],
                row["user_id"],
                row["id"],
            )
            listings.append(item)
        return listings

    def find(self, listing_id):
        rows = self._connection.execute(
            "SELECT * from listings WHERE id = %s", [listing_id]
        )
        row = rows[0]
        return Listing(
            row["name"],
            row["dates_available"],
            row["price"],
            row["image_url"],
            row["description"],
            row["user_id"],
            row["id"],
        )

    def create(self, listing):
        self._connection.execute(
            "INSERT INTO listings (name, dates_available, price, image_url, description, user_id) VALUES (%s, %s, %s, %s, %s, %s)",
            [
                listing.name,
                listing.dates_available,
                listing.price,
                listing.image_url,
                listing.description,
                listing.user_id,
            ],
        )
        return None

    def delete(self, listing_id):
        self._connection.execute("DELETE FROM listings WHERE id = %s", [listing_id])
        return None
