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


## deploy

서버 정보를 담고 있는 deploy/server.py 파일과 fabric이 필요합니다.

server.py 파일 예제.

``` python
# deploy/server.py

from fabric.api import env

env.pycon_user = 'username'
env.pycon_host = '123.456.789.012'
env.pycon_port = '1234'
```

fabric

``` shell
$ fab deploy --set=target=dev
# or
$ fab deploy --set=target=www
```
