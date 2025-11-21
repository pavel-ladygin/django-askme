from django.shortcuts import render
from .models import Question, Tag, Answer  
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
    return render(request,"pages/index.html", {
        "page_obj" : page_obj,
        "popular_tags" : popular_tags
        })

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question = Question.objects.by_id(pk)
    answers = Answer.objects.for_question(question)
    popular_tags = Tag.objects.popular(10)
    page_obj = paginate(request, answers, 5)
    return render(request, "pages/question_detail.html", {
        "page_obj" : page_obj,
        "question" : question,
        "popular_tags" : popular_tags
        })



def ask(request):
    popular_tags = Tag.objects.popular(10)
    return render(request, "pages/ask.html",{
        "popular_tags" : popular_tags,
        })

def login(request):
    popular_tags = Tag.objects.popular(10)
    return render(request, "pages/login.html",{
        "popular_tags" : popular_tags,
        })

def register(request):
    popular_tags = Tag.objects.popular(10)
    return render(request, "pages/register.html",{
        "popular_tags" : popular_tags
        })

def hot(request):
    questions = Question.objects.hot()
    popular_tags = Tag.objects.popular(10)
    page_obj = paginate(request,questions, 10)
    return render(request, "pages/hot.html",{
        "page_obj" : page_obj,
        "popular_tags" : popular_tags
        })

def tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    popular_tags = Tag.objects.popular(10)
    questions = Question.objects.by_tag(tag_slug)
    page_obj = paginate(request, questions, 10)
    tag = Tag.objects.slug_to_name(tag_slug)

    return render(request, "pages/tag.html",{
        "page_obj" : page_obj,
        "tag" : tag,
        "popular_tags" : popular_tags
          })
    


def edit_profile(request):
    popular_tags = Tag.objects.popular(10)
    return render(request, "pages/profile.html",{
        "popular_tags" : popular_tags
        })