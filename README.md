# Project Setup Guide
This guide provides instructions for setting up the project on Windows and MacOS.

**(Optional)** Delete the existing migrations if setting up on a new device.
Delete the existing database.
Invalidate the cache.

Open the terminal and follow these steps: 
# Install Django:
  - pip install django
# Install required dependencies:
  - pip install openpyxl
  - pip install reportlab
  - pip install django_extensions

# Run database migrations:
  - python manage.py makemigrations inventory
  - python manage.py migrate

# Populate the equipment database:
 - python manage.py populate_equipment

# Create a superuser account:
 - python manage.py createsuperuser

# Start the development server:
 - python manage.py runserver
