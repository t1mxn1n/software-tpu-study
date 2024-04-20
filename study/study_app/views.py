from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]


def index(request):

    data = {
        'title': 'Главная страница',
        'menu': menu,
    }

    return render(request, 'study_app/index.html', context=data)


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

    return render(request, 'study_app/ads.html', context=data)
