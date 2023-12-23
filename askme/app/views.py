import datetime

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect

from app.forms import (LoginForm, ProfileRegisterForm, UserRegisterForm,
                       ProfileSettingForm, AnswerForm, QuestionForm)
from app.models import *
from django.contrib.auth import login, authenticate



def paginate(request, objects, per_page=5):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page', 1)
    try:
        return paginator.page(page), paginator.num_pages
    except:
        return None


def index(request):
    questions = Question.objects.find_new_questions()
    if paginate(request, questions, 20) is None:
        return render(request, '404.html')

    paginate_result, pages_num = paginate(request, questions, 20)
    return render(request, 'index.html', {'questions': paginate_result,
                                          'req': '', 'page_obj': paginate_result, 'pages_num': pages_num})

def hot(request):
    questions = Question.objects.find_hot_questions()
    if paginate(request, questions, 20) is None:
        return render(request, '404.html')

    paginate_result, pages_num = paginate(request, questions, 20)
    return render(request, 'index.html', {'questions': paginate_result,
                                          'req': 'hot', 'page_obj': paginate_result, 'pages_num': pages_num})


def question(request, question_id=0):
    scroll_to_answer = False
    try:
        item = Question.objects.get(pk=question_id)
    except:
        return render(request, '404.html')

    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        answer = answer_form.save(commit=False)
        answer.author = request.user.profile
        answer.is_correct = 0
        answer.creation_date = datetime.datetime.now()
        answer.to_question = item
        answer.save()
        messages.success(request, 'Your answer was succesfully added!')
        scroll_to_answer = True

    answer_form = AnswerForm()
    answers = Answer.objects.find_answers_to_question(item)
    answers = sorted(answers, key=lambda one_answer: one_answer.answer_likes, reverse=True)
    if paginate(request, answers, 30) is None:
        return render(request, '404.html')

    paginate_result, pages_num = paginate(request, answers, 30)
    if scroll_to_answer:
        return redirect(f'/question/{question_id}/?page={pages_num}#{answer.id}')
    else:
        return render(request, 'question.html', {'question': item,
                                                              'answers': paginate_result, 'page_obj': paginate_result,
                                                              'pages_num': pages_num, 'form': answer_form})


def tag(request, tag_name):
    try:
        questions = Tag.objects.filter(tag_word=tag_name)[0].questions.all()
    except:
        return render(request, '404.html')

    if paginate(request, questions, 20) is None:
        return render(request, '404.html')
    paginate_result, pages_num = paginate(request, questions, 20)
    return render(request, 'index.html', {'questions': paginate_result,
                                          'req': tag_name, 'page_obj': paginate_result, 'pages_num': pages_num})

@login_required(login_url='/login/', redirect_field_name='continue')
def ask(request):
    question_form = QuestionForm()
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        question_model = question_form.save(commit=False)
        tags = request.POST.get('tag').split()
        tags_to_add = []
        for tag_text in tags:
            tag_model = Tag.objects.filter(tag_word=tag_text)
            if len(tag_model) == 0:
                tag_model = Tag()
                tag_model.tag_word = tag_text
                tag_model.save()
                tags_to_add.append(tag_model)
            else:
                tags_to_add.append(tag_model[0])

        question_model.author = request.user.profile
        question_model.creation_date = datetime.datetime.now()
        question_model.save()
        for tag_to_add in tags_to_add:
            question_model.tag.add(tag_to_add.id)
        return redirect(f'/question/{question_model.id}/')
    return render(request, 'ask.html', context={'form': question_form})

@csrf_protect
def logining(request):
    if request.method == "GET":
        login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)

                if request.GET.get('continue'):
                    return redirect(request.GET.get('continue'))
                return redirect('index')
            login_form.add_error(None, 'Wrong password or username!')
    return render(request, 'login.html', context={'form': login_form})

def logout(request):
    auth.logout(request)
    next_url = request.GET.get('next', '/')
    if 'edit' in next_url:
        next_url = '/'
    return redirect(next_url)

def signup(request):
    profile_form = ProfileRegisterForm()
    user_form = UserRegisterForm()
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                user = user_form.save()
                if user:
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.creation_date = user.date_joined
                    profile.save()
                    login(request, user)
                    return redirect('index')
                else:
                    user_form.add_error(field=None, error='User creation error!')
            except:
                user_form.add_error(field=None, error='This Username already exists!')

    return render(request, 'signup.html', context={'profile_form': profile_form, 'user_form': user_form})

@login_required(login_url='/login/', redirect_field_name='continue')
def user_settings(request):
    #setting_form = ProfileSettingForm()
    if request.method == 'POST':
        setting_form = ProfileSettingForm(request.POST)
        user = request.user
        old_username = user.username
        user.username = request.POST.get('username')
        user.profile.email = request.POST.get('email')
        user.profile.nickname = request.POST.get('nickname')
        try:
            user.save()
            user.profile.save()
            messages.success(request, 'Profile settings updated succesfully!')
        except:
            old_data = {
                'username': old_username,
                'email': request.user.profile.email,
                'nickname': request.user.profile.nickname
            }
            setting_form = ProfileSettingForm(initial=old_data)

    else:
        user_data = {
            'username': request.user.username,
            'email': request.user.profile.email,
            'nickname': request.user.profile.nickname
        }
        setting_form = ProfileSettingForm(initial=user_data)
    return render(request, 'userSettings.html', context={'setting_form': setting_form})