from calendar import monthrange
from datetime import datetime, timedelta

from celery import shared_task

from study.models import Course
from study.servises import send_mailing
from users.models import User


@shared_task
def mailing_about_updates(course_id):
    """Функция отправления сообщений об обновлении курса клиентам"""
    course = Course.objects.get(pk=course_id)
    now = datetime.now()
    expiration_date = now - timedelta(hours=4)

    if course.date_modified.timestamp() > expiration_date.timestamp():
        return

    course.date_modified = now
    course.save()
    subscription_list = course.subscription.all()
    user_list = [subscription.user for subscription in subscription_list]
    subject = 'Обновление'
    body = f'Вышло обновление по курсу {course}'
    send_mailing(user_list, subject, body)


@shared_task
def check_user():
    """Функция блокирования неактивных пользователей"""
    now = datetime.now()
    month = now.month
    year = now.year
    days_count = monthrange(year, month)
    user_list = User.objects.all()
    expiration_date = now - timedelta(days=days_count[1])
    for user in user_list:
        if user.last_login:
            if expiration_date.timestamp() >= user.last_login.timestamp():
                user.is_active = False
                user.save()
