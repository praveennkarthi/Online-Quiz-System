from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("quiz/<int:quiz_id>/", views.take_quiz, name="take_quiz"),
    path("result/<int:attempt_id>/", views.result, name="result"),
    path("my-results/", views.my_results, name="my_results"),
    path("quiz/<int:quiz_id>/leaderboard/", views.leaderboard, name="leaderboard"),
]
