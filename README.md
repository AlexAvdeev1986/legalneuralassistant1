# legalneuralassistant
 legalneuralassistant
1.
python -m venv venv
2.
source venv/bin/activate
pip install -r requirements.txt


django-admin startproject legal_assistant
cd legal_assistant
django-admin startapp legal_app

cd legal_assistant
touch .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver

