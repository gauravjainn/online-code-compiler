## Online Code Compile

#### Install dependencies
```sh
pip install -r requirements.txt
```

#### For local server, create a file local_settings.py with below content
```sh
DEBUG = True
ALLOWED_HOSTS = [] if DEBUG else ['*']
```

```sh
python manage.py migrate
python manage.py runserver
```

