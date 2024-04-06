from allauth.account.forms import SignupForm
from string import hexdigits
import random

from django.conf import settings
from django.core.mail import send_mail


from products.models import Author


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        Author.objects.create(user=user)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, k=5))
        user.code = code
        user.save()

        send_mail(
            subject=f'Код потверждения',
            message=f'{user.username}, Ваш код активации: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user

    # def save(self, request):
    #     user = super().save(request)
    #
    #     send_mail(
    #         subject='Добро пожаловать в наш интернет-магазин!',
    #         message=f'{user.username}, вы успешно зарегистрировались!',
    #         from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
    #         recipient_list=[user.email],
    #     )
    #     return user