from django.test import TestCase
# from models import *

# Create your tests here.


class TestStudyApp(TestCase):

    def test_access_pages(self):
        response = self.client.get("/", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="index.html")

        response = self.client.get("/ads", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="ads.html")

        response = self.client.get("/lk", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="lk.html")

        response = self.client.get("/register", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="register.html")

        response = self.client.get("/login", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="login.html")

        response = self.client.get("/logout", follow=True)
        self.assertEquals(response.status_code, 200)


    # @classmethod
    # def setup_test_data(cls):
    #     Category.objects.crate(name="Программирование")
    #     LessonState.objects.create(name="Занятие подтверждено")

