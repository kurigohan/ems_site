ems_site
========

CS320 Project - Application for Event Management Database 

Requirements for Dev:

    - Django 1.5+
    - Python 2.7+
    - MySQL 5.5+
    - One of the following MySQL DB API Drivers:

        1. MySQLdb
        2. MySQL Connector/Python 
        See https://docs.djangoproject.com/en/dev/ref/databases/ for more info.


Before Running:

In ems_site/settings.py , update the following if needed.  

    DATABASES = {
        'default': {
            'NAME': 'ems_db',
            'ENGINE': 'mysql.connector.django';  
            'USER': 'root',
            'PASSWORD': '',
        }
    }

ENGINE setting: 
- use 'django.db.backends.mysql' if using MySQLdb driver
- use 'mysql.connector.django' if using MySQL Connector/Python


To Run :

    1. From the terminal, change to the ems_site directory
    2a. If first usage or changes to models were made, use the command 'python manage.py syncdb' to sync models to the mysql database
    2b. If new fields were added to any models, the database will need to be recreated before running syncdb 
    3. Use the command 'python manage.py runserver' to start the development server
    4. Enter the server ip in your web browser (default is 127.0.0.1:8000)  to visit the site