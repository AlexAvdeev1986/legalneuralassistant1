# legalneuralassistant
 legalneuralassistant

python -m venv venv

source venv/bin/activate
pip install -r requirements.txt


django-admin startproject legal_assistant
cd legal_assistant
django-admin startapp legal_app

cd legal_assistant
python manage.py makemigration
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver
