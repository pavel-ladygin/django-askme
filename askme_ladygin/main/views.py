from django.shortcuts import render,redirect, HttpResponse
from .models import Question, Tag, Answer  , Profile
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .forms import LoginForm, SingupForm, EditProfileForm, QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.utils.text import slugify


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

    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect(f'/question/{question.id}/')
    else:
        form = AnswerForm()

    answers = Answer.objects.for_question(question)
    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    page_obj = paginate(request, answers, 5)
    return render(request, "pages/question_detail.html", {
        "page_obj": page_obj,
        "question": question,
        "popular_tags": popular_tags,
        "top_users": top_users,
        "form": form,
    })


@login_required
def ask(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            # Обработка тегов из поля ввода тегов
            tags_input = form.cleaned_data.get('tags_input', '')
            if tags_input:
                tag_names = [name.strip().lower() for name in tags_input.split(',') if name.strip()]
                for tag_name in tag_names:
                    tag_slug = slugify(tag_name)
                    tag, created = Tag.objects.get_or_create(slug = tag_slug, name=tag_name)
                    question.tags.add(tag)
            return redirect(f'/question/{question.id}/')
    else:
        form = QuestionForm()
    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    return render(request, "pages/ask.html",{
        "popular_tags" : popular_tags,
        "top_users" : top_users,
        "form" : form
        })

def login_view(request):
    continue_url = request.GET.get("next", "/")
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            return redirect(continue_url)
    else:
        form = LoginForm()

    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    return render(request, "pages/login.html",{
        "popular_tags" : popular_tags,
        "top_users" : top_users,
        "form" : form
        })

def logout_view(request):
    continue_url = request.GET.get("next", "/")
    logout(request)
    return redirect(continue_url)

def singup(request):
    continue_ulr = request.GET.get("next", "/")
    if request.method == "POST":
        form = SingupForm(data = request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect(continue_ulr)
    else:
        form = SingupForm()

    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    return render(request, "pages/register.html",{
        "popular_tags" : popular_tags,
        "top_users" : top_users,
        "form" : form
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
    user = get_object_or_404(Profile, id=user_id).user
    questions = Question.objects.top_profiles(user_id)
    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    page_obj = paginate(request,questions, 10)
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

    return render(request, "pages/tag.html",{
        "page_obj" : page_obj,
        "tag" : tag,
        "popular_tags" : popular_tags,
        "top_users" : top_users
        })
    

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/profile")
    else:
        form = EditProfileForm(request.user)
    popular_tags = Tag.objects.popular(10)
    top_users = Profile.objects.active_users(10)
    return render(request, "pages/profile.html",{
        "popular_tags" : popular_tags,
        "top_users" : top_users,
        "form" : form
        })