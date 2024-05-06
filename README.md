# Project Setup Guide
This guide provides instructions for setting up the project on Windows and macOS.

# Windows

(Optional) If setting up on a new device, delete the existing migrations.
Delete the existing database.
Invalidate the cache.

# MacOS

Open the terminal and follow these steps:
a. Install Django:
pip install django
b. Install required dependencies:
pip install openpyxl
pip install reportlab
pip install django_extensions

Run database migrations:
python manage.py makemigrations inventory
python manage.py migrate

Populate the equipment database:
python manage.py populate_equipment

Create a superuser account:
python manage.py createsuperuser

Start the development server:
python manage.py runserver

Log in using the following credentials:

Username: taf
Password: lmao

You can log in as either an admin or a regular user.
