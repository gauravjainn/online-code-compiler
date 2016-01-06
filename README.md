## Online Code Compile

#### For local server, create a file local_settings.py with below content
```sh
DEBUG = True
ALLOWED_HOSTS = [] if DEBUG else ['*']
```
s
```sh
python manage.py migrate
python manage.py runserver
```

