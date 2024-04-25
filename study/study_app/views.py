from django.contrib.auth.decorators import login_required
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

    return render(request, 'index.html')


def ads(request, ad_id):
    return HttpResponse(f"<h1>Объявление № {ad_id}</h1>")


def ads_general(request):
    return render(request, 'ads.html')


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


class RegisterUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class RegisterView(FormView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        user.save()
        login(self.request, user)
        return super().form_valid(form)
