# MakersBnB Python Project Seed

This repo contains the seed codebase for the MakersBnB project in Python (using 
Flask and Pytest).

Someone in your team should "Use this template" to create a copy of the codebase on their GitHub account.
Everyone in the team should then clone that copy of the repo to their local machine.

> NOTE: If you encounter a `ModuleNotFound` error, deactivate and then reactivate your virtual env. If that doesn't help, please reach out to your coach.

## Setup

```shell
# Set up the virtual environment
; python -m venv makersbnb-venv

# Activate the virtual environment
; source makersbnb-venv/bin/activate 

# Install dependencies
(makersbnb-venv); pip install -r requirements.txt

# Install the virtual browser we will use for testing
(makersbnb-venv); playwright install
# If you have problems with the above, contact your coach

# Copy the example env file and fill it in with your local settings
(makersbnb-venv); cp .example.env .env

# Create the development and test databases
(makersbnb-venv); ./bin/setup_dbs.sh

# Run the tests (with extra logging)
(makersbnb-venv); pytest -sv

# Run the app
(makersbnb-venv); python app.py

# Now visit http://localhost:5001/index in your browser
```

## Environment variables

The app reads its configuration from environment variables instead of having database names hardcoded in the source. `.example.env` is the template, committed to the repo so everyone can see what variables are needed. `.env` is your own local copy with real values filled in. It is gitignored, so it never gets committed and everyone's local setup can differ without conflicts.

`.env` holds three variables:

- `APP_ENV`, set to `development` locally. The app switches to `test` mode automatically when running under pytest.
- `DATABASE_URL`, the connection string for your main development database.
- `TEST_DATABASE_URL`, the connection string for a separate, disposable database used only by the test suite.

`DATABASE_URL` and `TEST_DATABASE_URL` must point at different databases. The test suite drops and recreates tables between runs, so if they pointed at the same database, running the tests would wipe out your development data.

## Database setup script

`bin/setup_dbs.sh` reads `.env`, works out the database names from `DATABASE_URL` and `TEST_DATABASE_URL`, and creates them with `createdb` if they do not already exist. It is safe to run more than once. Run it any time after editing `.env`, or whenever you pull changes and are not sure your local databases are up to date.

---

In short, copy `.example.env` to `.env`, fill in your database URLs, then run `bin/setup_dbs.sh` to create the databases. This replaces the old workflow of manually running `createdb` and editing database names directly in `lib/database_connection.py`.
