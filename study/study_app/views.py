from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.contrib.auth.forms import UserCreationForm
import datetime
from datetime import timedelta
from pytz import timezone
from django.contrib.auth import logout, login, authenticate

from django.contrib.auth.models import User

from study_app.models import Category, Course, Lesson, LessonState, Feedback

# Create your views here.

def index(request):
    return render(request, 'index.html')


def ads_general(request):

    ads = Course.objects.all().values(
        'name', 'description', 'price', 'duration', 'category_id__name', 'teacher_id_id', 'id'
    )

    if request.method == "POST":
        form = request.POST

        if not request.user.id:
            return render(request, 'ads.html', context={'courses': ads,
                                                        'error': True,
                                                        'error_msg': f'Необходима авторизация для отрпавки заявки!'})

        if request.user.id and request.user.id == int(form.get("teacher_id")):
            return render(request, 'ads.html', context={'courses': ads,
                                                        'error': True,
                                                        'error_msg': f'Запись на свои курсы невозможна! '})

        if request.user.id and request.user.id != int(form.get("teacher_id")):

            check_lesson_exist = Lesson.objects.filter(
                student_id=request.user.id,
                course_id=form.get("id_course"),
                state_id=1
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

    ads = get_feedbacks(ads)

    return render(request, 'ads.html', context={'courses': ads})


def get_feedbacks(courses):
    feedbacks = Feedback.objects.all().values('lesson_id', 'rating', 'description', 'lesson_id__course_id', 'lesson_id__student_id__first_name', 'id')
    new_courses = []
    for course in courses:
        new_course = course
        new_course['feedbacks'] = []
        new_course['feedback_flag'] = False
        for fb in feedbacks:
            if fb['lesson_id__course_id'] == course['id']:
                new_course['feedbacks'].append(fb)
                new_course['feedback_flag'] = True
        new_courses.append(new_course)
    return new_courses


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
        if "create_course" in form:
            Course.objects.create(
                teacher_id=User(id=request.user.id),
                category_id=Category(id=form.get('cat_sel')),
                name=form.get('name'),
                description=form.get('description'),
                duration=form.get('duration'),
                price=int(form.get('price'))
            )
        elif "del_course" in form:
            if int(form.get('teacher_id')) == request.user.id:
                course = Course.objects.filter(id=form.get('id_course'))
                course.delete()
        elif "del_lesson" in form:
            if int(form.get('student_id')) == request.user.id:
                lesson = Lesson.objects.get(pk=form.get('lesson_id'))
                lesson.state_id = LessonState(id=3)
                lesson.save()
        elif "reject" in form:
            lesson = Lesson.objects.get(pk=form.get('lesson_id'))
            lesson.is_approved = False
            lesson.save()
        elif "approve" in form:
            lesson = Lesson.objects.get(pk=form.get('lesson_id'))
            lesson.is_approved = True
            lesson.save()
        elif "del_lesson_teacher" in form:
            lesson = Lesson.objects.get(pk=form.get('lesson_id'))
            lesson.state_id = LessonState(id=3)
            lesson.save()
        elif "feedback" in form:
            lesson = Lesson.objects.get(pk=form.get('lesson_id'))
            feedback = Feedback.objects.create(
                lesson_id=Lesson(id=form.get('lesson_id')),
                rating=form.get('rate'),
                description=form.get('description')
            )
            if feedback:
                lesson.feedback_done = True
                lesson.save()

    check_expires_lessons()

    lessons_as_student_to_html = prettify_lessons({"student_id": request.user.id, "state_id": 1})
    lessons_as_teacher_to_html = prettify_lessons({"course_id__teacher_id": request.user.id, "state_id": 1})
    expires_lessons_to_html_for_student = prettify_lessons({"student_id": request.user.id, "state_id": 2})

    data = {
        'category': Category.objects.all().values(),
        'courses': Course.objects.filter(teacher_id=request.user.id).values(
            'name', 'description', 'price', 'duration', 'category_id__name', 'teacher_id_id', 'id'
        ),
        'lessons_as_student': lessons_as_student_to_html,
        'lessons_as_teacher': lessons_as_teacher_to_html,
        'expires_lessons_to_html_for_student': expires_lessons_to_html_for_student
    }
    return render(request, 'lk.html', context=data)


def check_expires_lessons():
    lessons = Lesson.objects.all().values()
    for lesson in lessons:
        if datetime.datetime.now() > lesson['time_end'] and lesson['is_approved']:
            lesson_change = Lesson.objects.get(pk=lesson['id'])
            lesson_change.state_id = LessonState(id=2)
            lesson_change.save()


def prettify_lessons(kwargs):
    lessons_orm = Lesson.objects.filter(**kwargs).values(
        'time_start', 'time_end', 'course_id__name', 'course_id__price', 'course_id__description',
        'course_id__category_id__name', 'is_approved', 'id', 'student_id', 'student_id__last_name',
        'student_id__first_name', 'student_id__email', 'comment', 'feedback_done'
    )
    lessons = []
    for les in lessons_orm:
        les['prettify_date'] = f'{les["time_start"].strftime("%d.%m.%Y")}'
        les['prettify_time'] = f'{les["time_start"].strftime("%H:%M")} - {les["time_end"].strftime("%H:%M")}'
        lessons.append(les)
    return lessons


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
