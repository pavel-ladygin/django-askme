from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("question/", views.question_detail),
    path("ask/",views.ask),
    path("login/", views.login),
    path("register/", views.register),
]
