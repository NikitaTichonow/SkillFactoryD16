from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Reply
from .tasks import reply_created_task, confirm_reply_task


# оповещение автора объявления о новом отклике
@receiver(post_save, sender=Reply)
def reply_created(instance, **kwargs):
    reply_created_task.delay(instance.pk)


# оповощение пользователя о принятии/отклонении его отклика
@receiver(post_save, sender=Reply)
def confirm_reply(instance, created=False, **kwargs):
    confirm_reply_task.delay(instance.pk)