from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("question/<int:pk>/", views.question_detail, name="question"),
    path("ask/",views.ask, name="ask"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.singup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("hot/", views.hot, name="hot"),
    path("tag/<slug:tag_slug>/", views.tag, name="tag"),
    path("profile/", views.edit_profile, name="profile"),
    path("user_questions/<user_id>", views.active_users, name = "user_questions"),
    path('ajax/toggle_question_vote/', views.toggle_question_vote, name='toggle_question_vote'),
    path('ajax/toggle_answer_vote/', views.toggle_answer_vote, name='toggle_answer_vote'),
    path('ajax/mark_answer_correct/', views.mark_answer_correct, name='mark_answer_correct'),
    path('ajax/unmark_answer_correct/', views.unmark_answer_correct, name='unmark_answer_correct'),
]
