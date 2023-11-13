from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import *


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
        return render(request, 'notFound.html')

    paginate_result, pages_num = paginate(request, questions, 20)
    return render(request, 'index.html', {'questions': paginate_result,
                                          'req': '', 'page_obj': paginate_result, 'pages_num': pages_num})


def hot(request):
    questions = Question.objects.find_hot_questions()
    if paginate(request, questions, 20) is None:
        return render(request, 'notFound.html')

    paginate_result, pages_num = paginate(request, questions, 20)
    return render(request, 'index.html', {'questions': paginate_result,
                                          'req': 'hot', 'page_obj': paginate_result, 'pages_num': pages_num})


def question(request, question_id=0):
    try:
        item = Question.objects.get(pk=question_id)
    except:
        return render(request, 'notFound.html')

    answers = Answer.objects.find_answers_to_question(item)
    answers = sorted(answers, key=lambda answer: answer.answer_likes, reverse=True)
    if paginate(request, answers, 30) is None:
        return render(request, 'notFound.html')

    paginate_result, pages_num = paginate(request, answers, 30)
    return render(request, 'question.html', {'question': item,
                                             'answers': paginate_result, 'page_obj': paginate_result,
                                             'pages_num': pages_num})


def tag(request, tag_name):
    try:
        questions = Tag.objects.filter(tag_word=tag_name)[0].questions.all()
    except:
        return render(request, 'notFound.html')

    if paginate(request, questions, 20) is None:
        return render(request, 'notFound.html')
    paginate_result, pages_num = paginate(request, questions, 20)
    return render(request, 'index.html', {'questions': paginate_result,
                                          'req': tag_name, 'page_obj': paginate_result, 'pages_num': pages_num})


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')
