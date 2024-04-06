from django.urls import path

from .views import ConfirmUser


urlpatterns = [
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
]