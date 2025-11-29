from django.shortcuts import render, HttpResponse
from .models import Question, Tag, Answer  , Profile
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404



def paginate(request, obj_list, obj_per_page):
    page_number = request.GET.get("page", 1)
    paginator = Paginator(obj_list, obj_per_page)
    page_obj = paginator.get_page(page_number)

    page_obj.elided_page_range = paginator.get_elided_page_range(
        number=page_obj.number,
        on_each_side=3,
        on_ends=1
    )
    return page_obj
    


def home(request):
    questions = Question.objects.new()
    page_obj = paginate(request, questions, 10)
    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    return render(request,"pages/index.html", {
        "page_obj" : page_obj,
        "popular_tags" : popular_tags,
        "top_users" : top_users
        })

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question = Question.objects.by_id(pk)
    answers = Answer.objects.for_question(question)
    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    page_obj = paginate(request, answers, 5)
    return render(request, "pages/question_detail.html", {
        "page_obj" : page_obj,
        "question" : question,
        "popular_tags" : popular_tags,
        "top_users" : top_users
        })



def ask(request):
    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    return render(request, "pages/ask.html",{
        "popular_tags" : popular_tags,
        "top_users" : top_users
        })

def login(request):
    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    return render(request, "pages/login.html",{
        "popular_tags" : popular_tags,
        "top_users" : top_users
        })

def register(request):
    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    return render(request, "pages/register.html",{
        "popular_tags" : popular_tags,
        "top_users" : top_users
        })

def hot(request):
    questions = Question.objects.hot()
    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    page_obj = paginate(request,questions, 10)
    return render(request, "pages/hot.html",{
        "page_obj" : page_obj,
        "popular_tags" : popular_tags,
        "top_users" : top_users
        })


def active_users(request, user_id):
    questions = Question.objects.top_profiles(user_id)
    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    page_obj = paginate(request,questions, 10)
    user = Profile.objects.id_to_name(user_id)
    return render(request, "pages/user_questions.html", {
        "page_obj" : page_obj,
        "popular_tags" : popular_tags,
        "top_users" : top_users,
        "user" : user
    })


def tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    questions = Question.objects.by_tag(tag_slug)
    page_obj = paginate(request, questions, 10)
    tag = Tag.objects.slug_to_name(tag_slug)

    return render(request, "pages/tag.html",{
        "page_obj" : page_obj,
        "tag" : tag,
        "popular_tags" : popular_tags,
        "top_users" : top_users
        })
    


def edit_profile(request):
    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    return render(request, "pages/profile.html",{
        "popular_tags" : popular_tags,
        "top_users" : top_users
        })