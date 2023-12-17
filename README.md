# MRKT_BE

Creating Similar API Endpoints for MRKT App on PlayStore

# Notes

- The develop branch is a refactor for the master branch

# Setup

## First Time install locally

`virtualenv -p python3  envsource env/bin/activate`
`pip install -r requirements/local.txt`

Create .env file and provide secret key for the project and database configuration

### Generate secret key

`py manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())`

copy the key and place it in .env file

`python manage.py migrate
python manage.py runserver
python manage.py createsuperuser --email admin@example.com --username admin`

# Usage

Use the Endpoints for adding Products in Cart 
Go to Order and "post" to add your Order depending on Product inventory 
