from django.contrib.auth.decorators import login_required
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login, authenticate

from django.contrib.auth.models import User

# Create your views here.
menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]


def index(request):

    data = {
        'title': 'Главная страница',
        'menu': menu,
    }

    return render(request, 'index.html', context=data)


def ads(request, ad_id):
    return HttpResponse(f"<h1>Объявление № {ad_id}</h1>")


def ads_general(request):

    data_db = [
        {'id': 1, 'title': 'Математика', 'content': 'бим бим бам бам', 'is_published': True},
        {'id': 2, 'title': 'Физика', 'content': 'мы стреляем', 'is_published': True},
        {'id': 3, 'title': 'Химия', 'content': 'по кому?', 'is_published': True},
    ]

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
    }

    return render(request, 'ads.html', context=data)


def login_user(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = request.POST
        user = authenticate(request, username=form.get('username'), password=form.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('personal'))

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


@login_required
def personal(request):
    return render(request, 'lk.html')


def register(request):
    if request.method == 'POST':
        form = request.POST
        print(form)
    return render(request, 'register.html')
