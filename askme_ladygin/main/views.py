from django.shortcuts import render,redirect
from .models import Question, Tag, Answer, Profile, QuestionLike, AnswerLike, Votes
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .forms import LoginForm, SingupForm, EditProfileForm, QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from django.http import JsonResponse
try:
    from django.utils.http import is_safe_url
except ImportError:
    from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from django.urls import reverse


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

    # Проверяем, есть ли уже правильный ответ
    has_accepted_answer = question.answers.filter(is_accepted=True).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect(reverse('question', args=[question.id]))
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
        "has_accepted_answer": has_accepted_answer,
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
            return redirect(reverse('question', args=[question.id]))
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
    if continue_url and not is_safe_url(continue_url, allowed_hosts={request.get_host()}):
        continue_url = "/"
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
    if continue_url and not is_safe_url(continue_url, allowed_hosts={request.get_host()}):
        continue_url = "/"
    logout(request)
    return redirect(continue_url)

def singup(request):
    continue_url = request.GET.get("next", "/")
    if continue_url and not is_safe_url(continue_url, allowed_hosts={request.get_host()}):
        continue_url = "/"
    if request.method == "POST":
        form = SingupForm(data = request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect(continue_url)
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

@login_required
@require_POST
def toggle_question_vote(request):
    try:
        question_id = int(request.POST.get('question_id'))
        vote_type = request.POST.get('type') 
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid data'}, status=400)

    question = get_object_or_404(Question, id=question_id)


    like, created = QuestionLike.objects.get_or_create(
        user=request.user,
        question=question,
        defaults={'value': Votes.UP if vote_type == 'like' else Votes.DOWN}
    )

    if not created:
        if (like.value == Votes.UP and vote_type == 'like') or (like.value == Votes.DOWN and vote_type == 'dislike'):

            score_change = -like.value
            like.delete()
        else:
            score_change = (Votes.DOWN if like.value == Votes.UP else Votes.UP) - like.value
            like.value = Votes.DOWN if like.value == Votes.UP else Votes.UP
            like.save()
    else:
        score_change = like.value

    question.score += score_change
    question.save()

    return JsonResponse({
        'success': True,
        'new_score': question.score
    })


@login_required
@require_POST
def toggle_answer_vote(request):
    try:
        answer_id = int(request.POST.get('answer_id'))
        vote_type = request.POST.get('type')
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid data'}, status=400)

    answer = get_object_or_404(Answer, id=answer_id)

    like, created = AnswerLike.objects.get_or_create(
        user=request.user,
        answer=answer,
        defaults={'value': Votes.UP if vote_type == 'like' else Votes.DOWN}
    )

    if not created:
        if (like.value == Votes.UP and vote_type == 'like') or (like.value == Votes.DOWN and vote_type == 'dislike'):
            score_change = -like.value
            like.delete()
        else:
            score_change = (Votes.DOWN if like.value == Votes.UP else Votes.UP) - like.value
            like.value = Votes.DOWN if like.value == Votes.UP else Votes.UP
            like.save()
    else:
        score_change = like.value

    answer.score += score_change
    answer.save()

    return JsonResponse({
        'success': True,
        'new_score': answer.score
    })

@login_required
@require_POST
def mark_answer_correct(request):
    try:
        answer_id = int(request.POST.get('answer_id'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid data'}, status=400)

    answer = get_object_or_404(Answer, id=answer_id)

    if answer.question.author != request.user:
        return JsonResponse({'error': 'Only author can mark correct answer'}, status=403)

    Answer.objects.filter(question=answer.question, is_accepted=True).update(is_accepted=False)

    answer.is_accepted = True
    answer.save()

    return JsonResponse({
        'success': True
    })

@login_required
@require_POST
def unmark_answer_correct(request):
    try:
        answer_id = int(request.POST.get('answer_id'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid data'}, status=400)

    answer = get_object_or_404(Answer, id=answer_id)

    if answer.question.author != request.user:
        return JsonResponse({'error': 'Only author can unmark correct answer'}, status=403)

    if not answer.is_accepted:
        return JsonResponse({'error': 'Answer is not marked as correct'}, status=400)

    answer.is_accepted = False
    answer.save()

    return JsonResponse({
        'success': True
    })