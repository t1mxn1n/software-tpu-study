from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Course(models.Model):
    teacher_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.FloatField()
    duration = models.CharField(max_length=255)


class Category(models.Model):
    name = models.CharField(max_length=255)


class Lesson(models.Model):
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    is_approved = models.BooleanField()
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    comment = models.CharField(max_length=255, default='Отсутствует')


class Feedback(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    description = models.CharField(max_length=255)
