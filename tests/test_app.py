from playwright.sync_api import Page, expect

# Tests for your routes go here

"""
We can render the index page
"""
def test_get_index(page, test_web_address):
    page.goto(f"http://{test_web_address}/index")

    heading = page.locator("h1")
    expect(heading).to_have_text("Welcome to MakersBnB")

def test_get_travel_bookings(page, test_web_address):
    pass

    #page.goto(f"http://{test_web_address}/users/1/bookings")

    #title = page.locator("h1")

    #expect(title).to_have_text("Your Bookings")