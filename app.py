import os
from flask import Flask, request, render_template, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from lib.database_connection import get_flask_database_connection
from lib.listing_repository import ListingRepository
from lib.user import User
from lib.user_repository import UserRepository


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def get_index():
    return render_template("index.html")


@app.route("/signup", methods=["GET"])
def get_signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
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
    repository.create(user)

    flash("Signed up successfully!")
    return redirect("/")

@app.route('/signin', methods=['GET'])
def get_signin():
  return render_template('signin.html')

@app.route('/signin', methods=['POST'])
def sign_in():
  email = request.form['email']
  password = request.form['password']

  connection = get_flask_database_connection(app)
  repository = UserRepository(connection)
  user = repository.find_by_email(email)

  if user is not None and check_password_hash(user.password, password):
    flash("Sign in successful")
    return redirect('/')
  else:
    return render_template('signin.html', error="invalid email or password, please try again."), 401



@app.route("/listings", methods=["GET"])
def get_listings():
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)
    listings = repository.all()
    return render_template("listings.html", listings=listings)


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
