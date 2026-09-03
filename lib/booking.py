class Booking:
    def __init__(self, start_date, end_date, status, listing_id, user_id, id =None):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.listing_id = listing_id
        self.user_id = user_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"The Booking details: ({self.start_date}_{self.end_date}, {self.status}, {self.listing_id}, {self.user_id})"
    

