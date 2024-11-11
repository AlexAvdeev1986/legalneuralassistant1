# legalneuralassistant
 legalneuralassistant
 
 # project structure
legal_assistant/
├── manage.py
├── requirements.txt
├── .env
├── legal_assistant/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── legal_app/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── forms.py
    ├── utils.py
    ├── templates/
    │   └── legal_app/
    │       ├── base.html
    │       ├── home.html
    │       ├── chat.html
    │       └── document_generator.html
    └── static/
        └── legal_app/
            ├── css/
            │   └── style.css
            └── js/
                └── main.js
 
 
1.
python -m venv venv
2.
source venv/bin/activate
pip install -r requirements.txt


django-admin startproject legal_assistant
cd legal_assistant
django-admin startapp legal_app

cd legal_assistant
создаем
touch .env
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=secret_key
DEBUG=True
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver

