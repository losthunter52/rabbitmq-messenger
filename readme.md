## Rabbitmq-Messenger

A simple messenger with Django and RabbitMQ with Django Threads.



### To Run:

Make sure you are in the root of the repository [...]/rabbitmq-messenger/"

1 - Create and run a venv
```bash
  python -m venv venv
  venv/scripts/activate
```

2 - Install pip and requirements
```bash
  python -m pip install --upgrade pip
  pip install -r requirements.txt
```

3 - Perform the migrations and collectstatic
```bash
  python manage.py makemigrations
  python manage.py migrate
  python manage.py collectstatic
```

4 - Configure the secret key in settings.py
```bash
  [...]
    SECRET_KEY = '(insert a django secret key here)'
  [...]
```

5 - Configure the rabbitmq server in connection.py
```bash
  [...]
     self.connection_type = 'A'
     self.host = ''
     self.port = ''
     self.route = ''
     self.login = ''
     self.password = ''
     self.url = ''
  [...]
```

6 - Run the server
```bash
  python manage.py runserver
```
