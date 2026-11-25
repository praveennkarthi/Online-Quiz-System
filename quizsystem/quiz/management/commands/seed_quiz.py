from django.core.management.base import BaseCommand
from quiz.models import Choice, Question, Quiz

DATA = {
    "title": "Python Basics",
    "description": "Check your core Python knowledge.",
    "time_limit_minutes": 5,
    "questions": [
        ("Which keyword defines a function in Python?", ["def", "func", "function", "lambda"], 0),
        ("What is the output type of 5 / 2 in Python 3?", ["int", "float", "str", "bool"], 1),
        ("Which data type is immutable?", ["list", "dict", "tuple", "set"], 2),
        ("Which command creates a new Django project?", ["django-admin startproject", "python new project", "django create", "pip startproject"], 0),
        ("Which Django file holds URL routes?", ["models.py", "urls.py", "views.py", "admin.py"], 1),
    ],
}


class Command(BaseCommand):
    help = "Create a sample quiz"

    def handle(self, *args, **options):
        quiz, _ = Quiz.objects.get_or_create(
            title=DATA["title"],
            defaults={
                "description": DATA["description"],
                "time_limit_minutes": DATA["time_limit_minutes"],
            },
        )
        if quiz.questions.exists():
            self.stdout.write("Sample quiz already exists.")
            return
        for text, choices, correct in DATA["questions"]:
            q = Question.objects.create(quiz=quiz, text=text)
            for i, c in enumerate(choices):
                Choice.objects.create(question=q, text=c, is_correct=(i == correct))
        self.stdout.write(self.style.SUCCESS("Sample quiz created."))
