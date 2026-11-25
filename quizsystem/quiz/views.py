from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SignUpForm
from .models import Attempt, AttemptAnswer, Choice, Quiz


def home(request):
    quizzes = Quiz.objects.prefetch_related("questions")
    return render(request, "quiz/home.html", {"quizzes": quizzes})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = list(quiz.questions.prefetch_related("choices"))

    if request.method == "POST":
        score = 0
        attempt = Attempt.objects.create(
            user=request.user, quiz=quiz, score=0, total=len(questions)
        )
        for q in questions:
            choice_id = request.POST.get(f"question_{q.id}")
            selected = None
            correct = False
            if choice_id:
                selected = Choice.objects.filter(pk=choice_id, question=q).first()
                correct = bool(selected and selected.is_correct)
            score += int(correct)
            AttemptAnswer.objects.create(
                attempt=attempt, question=q, selected=selected, is_correct=correct
            )
        attempt.score = score
        attempt.save()
        return redirect("result", attempt_id=attempt.id)

    return render(request, "quiz/take_quiz.html", {"quiz": quiz, "questions": questions})


@login_required
def result(request, attempt_id):
    attempt = get_object_or_404(Attempt, pk=attempt_id, user=request.user)
    answers = attempt.answers.select_related("question", "selected").prefetch_related(
        "question__choices"
    )
    return render(request, "quiz/result.html", {"attempt": attempt, "answers": answers})


@login_required
def my_results(request):
    attempts = Attempt.objects.filter(user=request.user).select_related("quiz")
    return render(request, "quiz/my_results.html", {"attempts": attempts})


def leaderboard(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    rows = (
        Attempt.objects.filter(quiz=quiz)
        .values("user__username")
        .annotate(best=Max("score"))
        .order_by("-best")[:10]
    )
    return render(request, "quiz/leaderboard.html", {"quiz": quiz, "rows": rows})
