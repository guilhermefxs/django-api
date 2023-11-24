# django-api

## Docs
You can find the api documentation on ./projectapi/documentation

## How to run

Create a virtual environment to isolate our package dependencies locally

`python3 -m venv env`
`source env/bin/activate` || On Windows use `env\Scripts\activate`

Install the dependencies
`pip install -r requirements.txt`

Go to the projectapi directory
`cd projectapi`

Run the api
`python manage.py runserver`

You can also create a super user, so you have access to /admin
`python manage.py createsuperuser`