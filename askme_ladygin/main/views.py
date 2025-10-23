from django.shortcuts import render, HttpResponse
import random
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



tags = ["python", "java", "django", "sql", "docker", "js", "react", "assembler"]
authors = ["pupkin", "ivanov", "upanov", "shurpatov", "vasiliy", "petrov", "rusakov"]
time = ["1 час", "2 часа", "2 дня", "5 дней", "1 год" , "5 лет"]


def make_fake_questions(n, seed) -> list:
    rnd = random.Random(seed)
    fake_questions = []
    for i in range(n):
        cur = {
            "id" : i,
            "title" : f"Название вопроса номер {i}",
            "text" : f"Описание вопроса {i}, что то должно быть написано",
            "tags" : [tags[rnd.randint(0, len(tags)/2)], tags[rnd.randint(len(tags)/2, len(tags)-1)]],
            "ansver_count" : rnd.randint(0, 10),
            "views" : rnd.randint(1, 1000),
            "score" : rnd.randint(-5, 100),
            "author" : authors[rnd.randint(0, len(authors)-1)],
            "created" : f"{time[rnd.randint(0, len(time)- 1)]} назад",
        }
        fake_questions.append(cur)
    return fake_questions

def make_fake_answers(pk, n, seed) -> list:
    rnd = random.Random(seed)
    fake_ansvers = []
    for i in range(n):
        cur = {
            "id" : i,
            "text" : f"Какой то текст {i}-го ответа на вопрос номер {pk}",
            "author" : authors[rnd.randint(0, len(authors)-1)],
            "created" : f"{time[rnd.randint(0, len(time)- 1)]} назад",
            "score" : rnd.randint(-5, 100),
            "is_accepted": rnd.choice([True, False])
        }
        fake_ansvers.append(cur)
    return fake_ansvers

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
    questions = make_fake_questions(100, 25)
    questions = sorted(questions, key=lambda q: q["id"], reverse=True)

    page_obj = paginate(request, questions, 10)
    return render(request,"pages/index.html", {"page_obj" : page_obj})

def question_detail(request, pk):
    questions = make_fake_questions(100, 25)
    questions = sorted(questions, key=lambda q: q["id"], reverse=True)
    flag = False
    question = {}
    for q in questions:
        if q["id"] == pk:
            flag = True
            question = q
            break
    if not flag:
        return render(request, "pages/404.html", status=404)
    
    answers = make_fake_answers(pk, 20, 25)
    answers = sorted(answers, key=lambda a: a["score"], reverse=True)
    page_obj = paginate(request, answers, 5)
    return render(request, "pages/question_detail.html", {"page_obj" : page_obj, "question" : question})



def ask(request):
    return render(request, "pages/ask.html")

def login(request):
    return render(request, "pages/login.html")

def register(request):
    return render(request, "pages/register.html")

def hot(request):
    questions = make_fake_questions(100, 25)
    questions = sorted(questions, key=lambda q: q["score"], reverse=True)
    page_obj = paginate(request,questions, 10)
    return render(request, "pages/hot.html", {"page_obj" : page_obj})

def tag(request, tag):
    questions = make_fake_questions(100, 25)
    verified_questions = []
    for q in questions:
        if tag in q["tags"]:
            verified_questions.append(q)
    verified_questions = sorted(verified_questions, key=lambda q: q["id"], reverse=True)
    page_obj = paginate(request, verified_questions, 10)

    return render(request, "pages/tag.html", {"page_obj" : page_obj, "current_tag" : tag})

def edit_profile(request):
    return render(request, "pages/profile.html")