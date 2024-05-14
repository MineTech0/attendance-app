# Webapp for creating attendance pdf files for courses

## How to run the app

1. Clone the repository
2. Run `poetry install` to install the dependencies
3. Run `poetry run python app.py` to start the app

## How to use the app

1. Go to `http://localhost:5000/`
2. Fill the form
3. Click on the `Generate PDF` button

The csv file must have column `name` that contain all the names of the students.