from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    """Модель таблицы - курсы"""
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Превью')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """Модель таблицы - уроки"""
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Превью')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    video_url = models.URLField(max_length=200, verbose_name='Ссылка на видео')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
