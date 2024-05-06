Project Setup Guide
This guide provides instructions for setting up the project on both Windows and macOS.
Windows

(Optional) If setting up on a new device, delete the existing migrations.
Delete the existing database.
Invalidate the cache.

macOS

Open the terminal and follow these steps:
a. Install Django:
Copy codepip install django
b. Install required dependencies:
Copy codepip install openpyxl
pip install reportlab
pip install django_extensions

Run database migrations:
Copy codepython manage.py makemigrations inventory
python manage.py migrate

Populate the equipment database:
Copy codepython manage.py populate_equipment

Create a superuser account:
Copy codepython manage.py createsuperuser

Start the development server:
Copy codepython manage.py runserver

Log in using the following credentials:

Username: taf
Password: lmao

You can log in as either an admin or a regular user.
