def test_about_page_renders(web_client):
    response = web_client.get("/about")

    assert response.status_code == 200
    assert b"About MakersBnB" in response.data


def test_about_page_lists_the_team(web_client):
    response = web_client.get("/about")

    assert b"Charlie Sampson" in response.data
    assert b"Emily Blackford" in response.data
    assert b"Erica Calogero" in response.data
    assert b"Kamilya Dosbayeva" in response.data
    assert b"Rochelle Ayad" in response.data
    assert b"Ryan Osmaston" in response.data
    assert b"Suleman Shah" in response.data


def test_about_page_links_to_github_profiles(web_client):
    response = web_client.get("/about")

    assert b"https://github.com/ChelleRB" in response.data
    assert b"https://github.com/Suleman28" in response.data
