# Generated by Django 5.0.4 on 2024-05-04 10:48

from django.db import migrations


def set_categories(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Category = apps.get_model('study_app', 'Category')
    if not Category.objects.all():
        Category.objects.create(name="Программирование")
        Category.objects.create(name="Дизайн")
        Category.objects.create(name="Иностранные языки")
        Category.objects.create(name="Музыка")
        Category.objects.create(name="Естественные науки")
        Category.objects.create(name="Другое")


def set_lesson_states(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Lesson = apps.get_model('study_app', 'LessonState')
    if not Lesson.objects.all():
        Lesson.objects.create(name="Занятие не проведено")
        Lesson.objects.create(name="Занятие проведено")
        Lesson.objects.create(name="Занятие удалено")


class Migration(migrations.Migration):

    dependencies = [
        ('study_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_categories),
        migrations.RunPython(set_lesson_states)
    ]
