import os
from flask import Flask, request, render_template, redirect, flash
from werkzeug.security import generate_password_hash
from lib.database_connection import get_flask_database_connection
from lib.user import User
from lib.user_repository import UserRepository
from lib.listing_repository import ListingRepository


# Create a new Flask app
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')

@app.route('/signup', methods=['GET'])
def get_signup():
  return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def create_account():
  name = request.form['name']
  email = request.form['email']
  password = request.form['password']
  password_confirmation = request.form['password_confirmation']

  if password != password_confirmation:
    return render_template('signup.html', error="Passwords do not match"), 400

  connection = get_flask_database_connection(app)
  repository = UserRepository(connection)

  hashed_password = generate_password_hash(password)
  user = User(name, email, hashed_password)
  repository.create(user)

  flash("Signed up successfully!")
  return redirect('/')

@app.route('/home', methods=['GET'])
def get_home():
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)
    listings = repository.all()
    return render_template('home.html', listings=listings)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
