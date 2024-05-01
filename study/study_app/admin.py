from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Lesson)
admin.site.register(Feedback)
admin.site.register(Course)
admin.site.register(LessonState)
# Register your models here.
