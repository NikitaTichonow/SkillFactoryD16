from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta

from accounts.models import User
from .models import Reply, Ad


# оповещение автора объявления о новом отклике
@shared_task
def reply_created_task(reply_id):
    reply = Reply.objects.get(pk=reply_id)
    email = reply.ad.author.user.email

    subject = f'На ваше объявление оставили отклик'

    text_content = (
        f'На ваше объявление "{reply.ad.title}" пользователь {reply.user} оставил отклик'
        f'Ссылка на отклик:  http://127.0.0.1:8000/{reply.get_absolute_url()}'
    )

    html_content = (
        f'На ваше объявление <a href="http://127.0.0.1:8000{reply.get_absolute_url()}">'
        f'{reply.ad.title}</a> пользователь {reply.user} оставил отклик <br>'
        f'<a href="http://127.0.0.1:8000{reply.get_absolute_url()}">'
        f'Зайдите посмотреть</a>'
    )

    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# оповощение пользователя о принятии/отклонении его отклика
@shared_task
def confirm_reply_task(reply_id):
    reply = Reply.objects.get(pk=reply_id)
    email = reply.user.email

    if reply.status == 'accepted':
        subject = f'Ваш отклик приняли'
        text_content = (
            f'Ваш отклик от {reply.published_date} на объявление "{reply.ad.title}" был принят {reply.ad.author.user}'
            f'Ссылка на объявление:  http://127.0.0.1:8000/{reply.get_absolute_url()}'
        )
        html_content = (
            f'Ваш отклик от {reply.published_date} на объявление <a href="http://127.0.0.1:8000{reply.get_absolute_url()}">'
            f'{reply.ad.title}</a> был принят {reply.ad.author.user}<br>'
            f'<a href="http://127.0.0.1:8000{reply.get_absolute_url()}">'
            f'Ссылка на объявление</a>'
        )
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    elif reply.status == 'rejected':
        subject = f'Ваш отклик отклонили'
        text_content = (
            f'Ваш отклик от {reply.published_date} на объявление "{reply.ad.title}" был отклонен {reply.ad.author.user}'
            f'Ссылка на объявление:  http://127.0.0.1:8000/{reply.get_absolute_url()}'
        )
        html_content = (
            f'Ваш отклик от {reply.published_date} на объявление <a href="http://127.0.0.1:8000{reply.get_absolute_url()}">'
            f'{reply.ad.title}</a> был отклонен {reply.ad.author.user}<br>'
            f'<a href="http://127.0.0.1:8000{reply.get_absolute_url()}">'
            f'Ссылка на объявление</a>'
        )
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


# еженедельная новостная рассылка с последними 15 объявлениями
@shared_task
def weekly_notification():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    ads = Ad.objects.filter(published_date__gte=last_week)[:15]
    emails = set(User.objects.all().values_list('email', flat=True))

    subject = f'Новые публикации за последнюю неделю:)'

    html_content = render_to_string(
        'email/week_email.html',
        {'ads': ads},
    )

    for email in emails:
        msg = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()