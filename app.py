import os
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from lib.database_connection import get_flask_database_connection
from lib.listing_repository import ListingRepository
from lib.listing import Listing
from lib.user import User
from lib.user_repository import UserRepository


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def get_index():
    return render_template("index.html")


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

    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    hashed_password = generate_password_hash(password)
    user = User(name, email, hashed_password)
    user_id = repository.create(user)

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

@app.route("/single_listing/<int:listing_id>", methods=["GET"])
def single_listing(listing_id):
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)
    listing = repository.find(listing_id)
    return render_template("single_listing.html", listing=listing)

@app.route("/listings/new", methods=["GET"])
def new_listing():
    if "user_id" not in session:
        flash("You must be logged in to create a listing")
        return redirect("/")
    return render_template("new_listing.html")

@app.route("/listings/new", methods={"POST"})
def create_listing():
    if "user_id" not in session:
        flash("You must be logged in to create a listing")
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
        flash(f"Failed to create listing: {str(e)}"), 401
        return redirect("/listings/new")

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
