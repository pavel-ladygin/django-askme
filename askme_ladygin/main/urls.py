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
    path("user_questions/<user_id>", views.active_users, name = "user_questions")
]
