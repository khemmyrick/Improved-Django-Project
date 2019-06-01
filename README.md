# Improved Django Project


## Instructions Overview
We spent a weekend doing a hackathon a year or so ago and someone built this project. It's...not the best. It runs kind of slow and has been a real pain to debug and add onto. We need you to go through the project, find where it's inefficient, and fix it. Check the templates for bad inheritance and extra database calls. Check the views for extra views or extra database calls. Check the models to make sure they're using the best fields. Check the forms for proper validation and fields. Basically just check the whole thing over. Oh, and it doesn't have any tests, so please get test coverage up to at least 75%.

## Setup
- After downloading files, create a virtualenv in the project folder.  
`python -m venv env`  
- Activate virtualenv.  
`env\scripts\activate`  
- Use pip to install requirements.  
`pip install -r requirements.txt`  
- From the primary backend folder, make migrations.  
`python manage.py makemigrations menu`
- Apply migrations.  
`python manage.py migrate`

## Running Tests
- User coverage to unit test the project.  
`coverage run --source='.' manage.py test menu`  
`coverage report`  
