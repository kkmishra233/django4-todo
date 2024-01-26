# Development

## Setup
```
pip install virtualenv

virtualenv venv

venv\\Scripts\\activate

cd src

pip install -r requirements.txt
```

## Run
```
python manage.py createsuperuser

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```