from django.shortcuts import render, HttpResponse
from random import randint
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



tags = ["python", "java", "c++", "django", "sql", "docker", "js", "react", "assembler"]
authors = ["pupkin", "ivanov", "upanov", "shurpatov", "vasiliy", "petrov", "rusakov"]
time = ["1 час", "2 часа", "2 дня", "5 дней", "1 год" , "5 лет"]

def make_fake_questions(n) -> list:
    fake_questions = []
    for i in range(n):
        cur = {
            "id" : i,
            "title" : f"Название вопроса номер {i}",
            "text" : f"Описание вопроса {i}, что то должно быть написано",
            "tags" : [tags[randint(0, len(tags)-1)], tags[randint(0, len(tags)-1)]],
            "ansver_count" : randint(0, 10),
            "views" : randint(1, 1000),
            "score" : randint(0, 100),
            "author" : authors[randint(0, len(authors)-1)],
            "created" : f"{time[randint(0, len(time)- 1)]} назад",
        }
        fake_questions.append(cur)
    return fake_questions


def paginate(request, obj_list, obj_per_page):
    page_number = request.GET.get("page", 1)
    paginator = Paginator(obj_list, obj_per_page)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj
    


def home(request):
    questions = make_fake_questions(100)
    page_obj = paginate(request, questions, 10)
    return render(request,"pages/index.html", {"page_obj" : page_obj})

def question_detail(request):
    return render(request, "pages/question.html")

def ask(request):
    return render(request, "pages/ask.html")

def login(request):
    return render(request, "pages/login.html")

def register(request):
    return render(request, "pages/register.html")

def hot(request):
    return render(request, "pages/index.html")

def tag(request):
    return render(request, "pages/index.html")