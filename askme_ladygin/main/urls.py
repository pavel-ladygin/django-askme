from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("question/<int:pk>/", views.question_detail, name="question"),
    path("ask/",views.ask, name="ask"),
    path("login/", views.login, name="login"),
    path("signup/", views.register, name="signup"),
    path("hot/", views.hot, name="hot"),
    path("tag/<slug:tag_slug>/", views.tag, name="tag"),
    path("profile/", views.edit_profile, name="profile"),
]
