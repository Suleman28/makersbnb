class Listing:
    def __init__(self, name, dates_available, price, image_url, description, user_id, id =None):
        self.id = id
        self.name= name
        self.dates_available = dates_available
        self.price = price
        self.image_url = image_url
        self.description = description
        self.user_id = user_id


    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"The Listing's details: ({self.name}, {self.price}, {self.description})"
    
