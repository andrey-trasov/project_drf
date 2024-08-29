from celery import shared_task
from django.core.mail import send_mail

from lms.models import Subscription, Course
from myproject.settings import EMAIL_HOST_USER


@shared_task
def updating_course(course):
    subscriptions = Subscription.objects.filter(course=course)
    list_email = []
    for subscription in subscriptions:
        list_email.append(subscription.user.email)
    course = Course.objects.filter(id=course).first()
    print(course.name)
    send_mail(
        subject='Обновление курса',  # тема письма
        message=f'Курс {course.name} обновлен.',  # сообщение
        from_email=EMAIL_HOST_USER,  # с какого мейла отправляем
        recipient_list=list_email  # список имейлов на которые отправляем
    )