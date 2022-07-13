# covid_vis

Requirements:

1. Python 3.6 or higher (Refer to this link to download and install Python: https://www.python.org/downloads/release/python-366/)
2. Pip (Python package manager) usually gets installed along with python. If pip is not installed on your machine then follow the instructions in this link to install pip: https://www.makeuseof.com/tag/install-pip-for-python/

## Steps to setup the project server locally (One time setup)

1. Clone the repository.
2. Navigate to the repository folder in your file system.
3. `pip install virtualenv`
4. Create virtual environment if required: `virtualenv venv`
5. Activate virtual environment: `source venv/bin/activate`
   In windows: `venv\Scripts\activate`
6. Run the following command : `pip install -r requirements.txt`
7. Create superuser by running following command:
   `python manage.py migrate`
   `python manage.py createsuperuser`
   Follow on screen instructions to create superuser by giving username and password.

## Steps to run development server locally

1. Run the python server : `python manage.py runserver 0.0.0.0:8000`

## Step to run production server using gunicorn

1. Run the gunicorn server `gunicorn covid_vis.wsgi --bind 0.0.0.0:8000`
