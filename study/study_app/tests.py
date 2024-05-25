from django.test import TestCase
from django.urls import reverse
from study_app.models import *
from http import HTTPStatus

# Create your tests here.


class TestStudyApp(TestCase):

    def setUp(self):
        self.test_user = {
            'first_name': 'test_user_first_name',
            'last_name': 'test_user_last_name',
            'email': 'test_user_email@test.com',
            'password1': 'Test_qwerty_8583',
            'password2': 'Test_qwerty_8583'
        }
        return super().setUp()

    def test_models_get_mock_value(self):
        category = Category.objects.get(name="Программирование")
        state = LessonState.objects.get(name="Занятие не проведено")
        self.assertEquals(category.name, "Программирование")
        self.assertEquals(state.name, "Занятие не проведено")

    def test_access_pages(self):
        response = self.client.get("/", follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name="index.html")

        response = self.client.get("/ads", follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name="ads.html")

        response = self.client.get("/register", follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name="registration/register.html")

        response = self.client.get("/login", follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name="login.html")

        response = self.client.get("/logout", follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_register(self):

        response = self.client.post(reverse("register"), self.test_user,  format="text/html")
        self.assertEquals(response.status_code, HTTPStatus.FOUND)

        response_lk = self.client.get("/lk", follow=True)
        self.assertEquals(response_lk.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response_lk, template_name="lk.html")

    def test_create_course(self):
        self.client.post(reverse("register"), self.test_user, format="text/html")

        test_course = {
            "teacher_id": 1,
            "cat_sel": 1,
            "name": "test_course",
            "description": "test_course",
            "duration": "test_course",
            "price": '10000',
            "create_course": "Submit"
        }

        self.client.post(reverse("personal"), test_course)
        data = Course.objects.all()
        self.assertEquals(data[0].name, "test_course")
