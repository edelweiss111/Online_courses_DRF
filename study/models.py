from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    """Модель таблицы - курсы"""
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Превью')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Владелец', default=1)

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
    video_url = models.URLField(max_length=200, **NULLABLE, verbose_name='Ссылка на видео')

    course = models.ForeignKey('Course', on_delete=models.SET_NULL, **NULLABLE, verbose_name='Курс',
                               related_name='lesson')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Владелец', default=1)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payment(models.Model):
    """Модель таблицы - платежи"""

    class PaymentType(models.TextChoices):
        CASH = "CASH", "Наличные"
        TRANSFER_TO_ACCOUNT = 'TRANSFER_TO_ACCOUNT', 'Перевод на счет'

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='payment_list')
    pay_date = models.DateField(auto_now_add=True, verbose_name='Дата платежа')
    paid_course = models.ForeignKey('Course', on_delete=models.CASCADE, **NULLABLE, verbose_name='Оплаченный курс',
                                    related_name='payment')
    paid_lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, **NULLABLE, verbose_name='Оплаченный урок',
                                    related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, verbose_name="Способ оплаты")

    def __str__(self):
        return f'{self.user} - {self.pay_date}'

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    paid_course__isnull=True,
                    paid_lesson__isnull=False
                ) | models.Q(
                    paid_course__isnull=False,
                    paid_lesson__isnull=True
                ),
                name='one_of_course_or_lesson_have_to_be_set'
            )
        ]
