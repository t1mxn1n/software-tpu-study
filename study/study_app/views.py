from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
import datetime
from datetime import timedelta
from pytz import timezone
from django.contrib.auth import logout, login, authenticate

from django.contrib.auth.models import User

from study_app.models import Category, Course, Lesson

# Create your views here.
menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]


def index(request):

    return render(request, 'index.html')


def ads_general(request):

    ads = Course.objects.all().values(
        'name', 'description', 'price', 'duration', 'category_id__name', 'teacher_id_id', 'id'
    )

    if request.method == "POST":
        form = request.POST

        if request.user.id and request.user.id == int(form.get("teacher_id")):
            return render(request, 'ads.html', context={'courses': ads,
                                                        'error': True,
                                                        'error_msg': f'Запись на свои курсы невозможна! '})

        if request.user.id and request.user.id != int(form.get("teacher_id")):

            check_lesson_exist = Lesson.objects.filter(
                student_id=request.user.id,
                course_id=form.get("id_course")
            )

            if check_lesson_exist:
                return render(request, 'ads.html', context={'courses': ads,
                                                            'error': True,
                                                            'error_msg': f'У вас уже есть заявка на курс "{Course.objects.get(pk=form.get("id_course")).name}"!'})

            time_start = datetime.datetime.strptime(f"{form.get('date')} {form.get('time')}", "%Y-%m-%d %H:%M")
            time_end = time_start + timedelta(hours=1)
            Lesson.objects.create(
                is_approved=False,
                time_start=time_start,
                time_end=time_end,
                course_id=Course(id=form.get("id_course")),
                student_id=User(id=request.user.id),
                comment=form.get('comment') if form.get('comment') else 'Отсутствует'
            )

            return render(request, 'ads.html', context={'courses': ads,
                                                        'success': True,
                                                        'msg': f'Заявка на занятие по "{Course.objects.get(pk=form.get("id_course")).name}" успешно создана!'})

    return render(request, 'ads.html', context={'courses': ads})


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

    if request.method == 'POST':
        form = request.POST
        if len(form) == 6:
            Course.objects.create(
                teacher_id=User(id=request.user.id),
                category_id=Category(id=form.get('cat_sel')),
                name=form.get('name'),
                description=form.get('description'),
                duration=form.get('duration'),
                price=int(form.get('price'))
            )
        elif len(form) == 3:

            if int(form.get('teacher_id')) == request.user.id:
                course = Course.objects.filter(id=form.get('id_course'))
                course.delete()

    data = {
        'category': Category.objects.all().values(),
        'courses': Course.objects.filter(teacher_id=request.user.id).values(
            'name', 'description', 'price', 'duration', 'category_id__name', 'teacher_id_id', 'id'
        )
    }
    return render(request, 'lk.html', context=data)


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
