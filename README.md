# back.ih.by

This app tested on ubuntu 24.04, python 3.12

To run this app:
+ install python3, pip3, python3-venv
+ copy this project 
+ cd project/dj
+ python3 -m venv venv
+ source venv/bin/activate (activate virtual enviroment)
+ pip3 install -r requirements.txt (install dependencies)
+ python3 manage.py migrate
+ python3 manage.py createsuperuser
+ python3 manage.py runserver {ip:port|port}
+ ./manage.py migrate (apply migrations for DB, if you need)
+ ./manage.py loaddata fixture/department.json (if you run at first)
+ ./manage.py loaddata fixture/imns.json (if you run at first)
+ ./manage.py loaddata fixture/user.json (if you run at first)
+ ./manage.py runsever {ip:port} (start app)


***.env:***

SECRET_KEY=

DEBUG=

ALLOWED_HOSTS=*

DB_ENGINE='django.db.backends.mysql'

DB_NAME=''

DB_USER=''

DB_PASSWORD=''

DB_HOST='127.0.0.1'

DB_PORT='3306'
