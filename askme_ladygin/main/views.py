from django.shortcuts import render, HttpResponse

def home(request):
    return render(request,"pages/index.html")

def question_detail(request):
    return render(request, "pages/question.html")

def ask(request):
    return render(request, "pages/ask.html")

def login(request):
    return render(request, "pages/login.html")

def register(request):
    return render(request, "pages/register.html")