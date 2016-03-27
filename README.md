A git repository for PyCon APAC/Korea 2016


## requirements

- Python 2.7.9


## development setting

```
$ git clone git@github.com:pythonkr/pyconapac-2016.git
$ cd pyconapac-2016
$ pip install -r requirements.txt
$ python manage.py compilemessages
$ python manage.py makemigrations  # flatpages
$ python manage.py migrate
$ python manage.py loaddata ./pyconkr/fixtures/flatpages.json
$ bower install
$ python manage.py runserver
```
