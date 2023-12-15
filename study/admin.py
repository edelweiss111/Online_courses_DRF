from django.contrib import admin

from study.models import Course, Lesson


@admin.register(Course)
class ContactAdmin(admin.ModelAdmin):
    """Админка отображения модели Course"""
    list_display = ('id', 'name', 'image', 'description')


@admin.register(Lesson)
class ContactAdmin(admin.ModelAdmin):
    """Админка отображения модели Lesson"""
    list_display = ('id', 'name', 'image', 'description', 'video_url')
