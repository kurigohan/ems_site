ems_site
========

CS320 Project - Application for Event Management Database 

Requirements:

    - Django 1.5+
    - Python 2.7+
    - MySQL 5.5+
    - One of the following MySQL DB API Drivers:

        1. MySQLdb
        2. MySQL Connector/Python 
        See https://docs.djangoproject.com/en/dev/ref/databases/ for more info.


Before Running:
In ems_site/settings.py , the update the following setting if needed.  

    DATABASES = {
        'default': {
            'NAME': 'ems_db', 
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'root', 
          #  'PASSWORD': '', 
        }
    }


To Run :

    1. From the terminal, change to the ems_site directory
    2. Use the command 'python manage.py syncdb' to sync django models to the database (if any model changes)
    3. Use the command 'python manage.py runserver' to start the developtment server
    4. Enter the server ip in your web browser (default is 127.0.0.1:8000)  to visit the site


Useful MySQL links:

    - Creating a mysql database
        http://dev.mysql.com/doc/refman/5.1/en/creating-database.html

    - Adding user accounts
        http://dev.mysql.com/doc/refman/5.1/en/adding-users.html