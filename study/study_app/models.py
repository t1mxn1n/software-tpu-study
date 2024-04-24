from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# class Course(models.Model):
#     teacher_id = models.IntegerField()
#     category_id = models.ForeignKey('Category', on_delete=models.PROTECT)
#     name = models.CharField(max_length=255)
#     description = models.CharField(max_length=255)
#     price = models.FloatField()
#     duration = models.CharField(max_length=255)
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=255)
#
#
# class Lesson(models.Model):
#     course_id = models.ForeignKey('Course', on_delete=models.PROTECT)
#     is_approved = models.BooleanField()
#     student_id = models.ForeignKey('Users', on_delete=models.PROTECT)
#     time_start = models.DateTimeField()
#     time_end = models.DateTimeField()
#


