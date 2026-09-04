import os
import re
from datetime import datetime
from flask import Flask, request, render_template, redirect, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from lib.database_connection import get_flask_database_connection
from lib.booking import Booking
from lib.booking_repository import BookingRepository
from lib.listing_repository import ListingRepository
from lib.listing import Listing
from lib.user import User
from lib.user_repository import UserRepository, EmailAlreadyRegisteredError
from lib.booking import Booking
from lib.booking_repository import BookingRepository


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")


# dates_available is stored as free text (e.g. "2027-01-01, 2028-12-12" or
# "2027-01-01 to 2028-12-12"), so this tolerates both known separators and
# falls back to the raw value if it can't be parsed.
@app.template_filter("friendly_dates")
def friendly_dates(raw):
    if not raw:
        return raw
    parts = re.split(r"\s*(?:,|\bto\b)\s*", raw.strip())
    if len(parts) != 2:
        return raw
    try:
        start, end = (datetime.strptime(p, "%Y-%m-%d") for p in parts)
    except ValueError:
        return raw
    return f"{start.day} {start.strftime('%b %Y')} – {end.day} {end.strftime('%b %Y')}"


# Booking start/end dates come from DATE columns as date objects, but tolerate
# an ISO string too. Falls back to the raw value if it can't be parsed.
@app.template_filter("friendly_date")
def friendly_date(value):
    if not value:
        return value
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return value
    return f"{value.day} {value.strftime('%b %Y')}"


def render_error(code, heading, message):
    return render_template("error.html", code=code, heading=heading, message=message), code


@app.errorhandler(403)
def forbidden(error):
    return render_error(403, "Forbidden", "You don't have permission to view this page.")


@app.errorhandler(404)
def page_not_found(error):
    return render_error(404, "Page not found", "Sorry, we couldn't find the page you're looking for.")


@app.errorhandler(405)
def method_not_allowed(error):
    return render_error(405, "Method not allowed", "That action isn't available on this page.")


@app.errorhandler(500)
def internal_server_error(error):
    return render_error(500, "Something went wrong", "Sorry, something broke on our end. Please try again.")


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def get_index():
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)
    listings = repository.select_for_fe(3)
    return render_template("index.html", listings=listings)


@app.route("/sign_up", methods=["GET"])
def get_signup():
    return render_template("signup.html")


@app.route("/sign_up", methods=["POST"])
def create_account():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    password_confirmation = request.form["password_confirmation"]
    if password != password_confirmation:
        return render_template("signup.html", error="Passwords do not match"), 400
    try:
        User.validate_password(password)
    except ValueError as e:
        return render_template("signup.html", error=str(e)), 400
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)
    hashed_password = generate_password_hash(password)
    user = User(name, email, hashed_password)
    try:
        user_id = repository.create(user)
    except EmailAlreadyRegisteredError:
        return render_template("signup.html", error="An account with that email already exists."), 400
    session['user_id'] = user_id
    flash("Signed up successfully!")
    return redirect("/")

@app.route('/sign_in', methods=['GET'])
def get_signin():
  return render_template('signin.html')

@app.route('/sign_in', methods=['POST'])
def create_session():
  email = request.form['email']
  password = request.form['password']

  connection = get_flask_database_connection(app)
  repository = UserRepository(connection)
  user = repository.find_by_email(email)

  if user is not None and check_password_hash(user.password, password):
    session['user_id'] = user.id
    flash("Sign in successful")
    return redirect('/')
  else:
    return render_template('signin.html', error="invalid email or password, please try again."), 401

@app.context_processor
def inject_current_user():
    if 'user_id' not in session:
        return {}
    connection = get_flask_database_connection(app)
    return {'current_user': UserRepository(connection).find(session['user_id'])}


@app.route('/sign_out', methods=['POST'])
def destroy_session():
    session.pop('user_id', None)
    flash('Successfully signed out.')
    return redirect('/')


@app.route("/listings", methods=["GET"])
def get_listings():
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)
    listings = repository.all()
    return render_template("listings.html", listings=listings)

@app.route("/listings/<int:listing_id>", methods=["GET"])
def single_listing(listing_id):
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)
    # find() indexes into the query result, so a missing listing raises
    # IndexError - turn that into a 404 rather than a 500.
    try:
        listing = repository.find(listing_id)
    except IndexError:
        abort(404)
    user_repository = UserRepository(connection)
    host = user_repository.find(listing.user_id)
    booking_repository = BookingRepository(connection)
    booked_bookings = booking_repository.find_booked_by_listing(listing_id)
    booked_ranges = [
        {
            "from": booking.start_date.isoformat() if hasattr(booking.start_date, "isoformat") else str(booking.start_date),
            "to": booking.end_date.isoformat() if hasattr(booking.end_date, "isoformat") else str(booking.end_date),
        }
        for booking in booked_bookings
    ]
    parts = [p.strip() for p in (listing.dates_available or "").split(",") if p.strip()]
    available_from = parts[0] if len(parts) > 0 else None
    available_to = parts[1] if len(parts) > 1 else None
    return render_template(
        "single_listing.html",
        listing=listing,
        host=host,
        booked_ranges=booked_ranges,
        available_from=available_from,
        available_to=available_to,
    )

@app.route("/users/<int:user_id>/listings", methods=["GET"])
def get_host_listings(user_id):
    if "user_id" not in session:
        flash("You must be logged in to view your listings")
        return redirect("/")
    if session["user_id"] != user_id:
        flash("You can only view your own listings")
        return redirect("/")
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)
    listings = [l for l in repository.all() if int(l.user_id) == int(user_id)]
    return render_template("host_listings.html", listings=listings)

@app.route("/users/<int:user_id>/listings/<int:listing_id>", methods=["GET"])
def get_host_listing(user_id, listing_id):
    if "user_id" not in session:
        flash("You must be logged in to view your listing")
        return redirect("/")
    if session["user_id"] != user_id:
        flash("You can only view your own listing")
        return redirect("/")
    connection = get_flask_database_connection(app)
    listing_repository = ListingRepository(connection)
    booking_repository = BookingRepository(connection)
    listing = listing_repository.find(listing_id)
    bookings = booking_repository.find_by_user(session['user_id'])
    return render_template("host_listing.html", listing=listing, bookings=bookings)

@app.route("/users/<int:user_id>/listings/new", methods=["GET"])
def new_listing(user_id):
    if "user_id" not in session:
        flash("You must be logged in to create a listing")
        return redirect("/")
    if session["user_id"] != user_id:
        flash("You can only create listings under your own account")
        return redirect("/")
    return render_template("new_listing.html")

@app.route("/users/<int:user_id>/listings/new", methods=["POST"])
def create_listing(user_id):
    if "user_id" not in session:
        flash("You must be logged in to create a listing")
        return redirect("/")
    if session["user_id"] != user_id:
        flash("You can only create listings under your own account")
        return redirect("/")
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)
    listing_name = request.form["listing_name"]
    listing_dates_available = request.form["listing_dates_available"]
    listing_price = request.form["listing_price"]
    listing_image_url = request.form["listing_image_url"]
    listing_description = request.form["listing_description"]
    listing_user_id = session["user_id"]
    try:
        repository.create(Listing(listing_name, listing_dates_available, listing_price, listing_image_url, listing_description, listing_user_id))
        flash("Listing created successfully")
        return redirect("/listings")
    except Exception as e:
        flash(f"Failed to create listing: {str(e)}")
        return redirect(f"/users/{user_id}/listings")

@app.route("/bookings", methods=["POST"])
def create_booking():
    if "user_id" not in session:
        flash("You must be logged in to request a booking")
        return redirect("/sign_in")

    listing_id = request.form["listing_id"]
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]

    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)

    if not repository.is_available(listing_id, start_date, end_date):
        flash("Those dates are already booked.", "error")
        return redirect(f"/listings/{listing_id}")

    booking = Booking(start_date, end_date, "PENDING", listing_id, session["user_id"])
    repository.create(booking)

    flash("Your booking request has been submitted.")
    return redirect(f"/listings/{listing_id}")


@app.route("/users/<int:user_id>/bookings", methods={"GET"})
def get_travel_bookings(user_id):
    if "user_id" not in session:
        flash("You must be logged in to view your bookings")
        return redirect("/")
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    listing_repository = ListingRepository(connection)
    bookings = booking_repository.find_by_user(session['user_id'])
    listings = []
    for booking in bookings:
       listing = listing_repository.find(booking.listing_id)
       listings.append(listing)
    return render_template("user_bookings.html", booking_pairs=list(zip(bookings, listings)))


@app.route("/users/<int:user_id>/listings/<int:listing_id>/bookings", methods=["GET"])
def get_listing_bookings(user_id, listing_id):
    if "user_id" not in session:
        flash("You must be logged in to view booking requests")
        return redirect("/")
    connection = get_flask_database_connection(app)
    listing_repository = ListingRepository(connection)
    listing = listing_repository.find(listing_id)
    if listing.user_id != session["user_id"]:
        flash("You can only view booking requests for your own listings")
        return redirect("/")
    booking_repository = BookingRepository(connection)
    bookings = booking_repository.find_all_listings(listing_id)
    return render_template("host_bookings.html", listing=listing, bookings=bookings)


@app.route("/listings/<int:listing_id>/bookings/<int:booking_id>", methods=["GET"])
def check_on_single_booking(listing_id, booking_id):
    if "user_id" not in session:
        flash("You must be logged in to view booking requests")
        return redirect("/")
    connection = get_flask_database_connection(app)
    listing_repository = ListingRepository(connection)
    listing = listing_repository.find(listing_id)
    if listing.user_id != session["user_id"]:
        flash("You can only view booking requests for your own listings")
        return redirect("/")
    booking_repository = BookingRepository(connection)
    booking = booking_repository.find(booking_id)
    if booking.listing_id != listing_id:
        flash("Booking not found for this listing")
        return redirect(f"/users/{session['user_id']}/listings/{listing_id}/bookings") #should hopefully work?
    return render_template("single_booking.html", listing=listing, booking=booking)

@app.route("/listings/<int:listing_id>/bookings/<int:booking_id>/approve", methods=["POST"])
def approve_booking(listing_id, booking_id):
    return update_booking_status(listing_id, booking_id, "BOOKED")

@app.route("/listings/<int:listing_id>/bookings/<int:booking_id>/deny", methods=["POST"])
def deny_booking(listing_id, booking_id):
    return update_booking_status(listing_id, booking_id, "DECLINED")

def update_booking_status(listing_id, booking_id, status):
    if "user_id" not in session:
        flash("You must be logged in to manage booking requests")
        return redirect("/")
    connection = get_flask_database_connection(app)
    listing_repository = ListingRepository(connection)
    listing = listing_repository.find(listing_id)
    if listing.user_id != session["user_id"]:
        flash("You can only manage bookings for your own listings")
        return redirect("/")
    booking_repository = BookingRepository(connection)
    booking = booking_repository.find(booking_id)
    if booking.listing_id != listing_id:
        flash("Booking not found for this listing")
        return redirect(f"/users/{session['user_id']}/listings/{listing_id}/bookings")
    booking_repository.update_booking_status_managed_by_host(booking_id, status)
    flash(f"Booking {status.lower()}")
    return redirect(f"/users/{session['user_id']}/listings/{listing_id}/bookings")

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
