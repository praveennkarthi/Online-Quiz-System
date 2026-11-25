# Online Quiz System (Django)

## Run
    python -m venv venv
    venv\Scripts\activate          # Windows  (Mac/Linux: source venv/bin/activate)
    pip install -r requirements.txt
    python manage.py makemigrations quiz
    python manage.py migrate
    python manage.py seed_quiz
    python manage.py createsuperuser
    python manage.py runserver

Open http://127.0.0.1:8000/  (admin panel: /admin/)

## Features
- Sign up / login / logout
- Admin adds quizzes, questions and choices
- Timed quiz (auto-submit when time ends)
- Auto scoring + answer review
- My Results history and per-quiz leaderboard
