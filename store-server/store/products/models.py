from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from accounts.models import User

from ckeditor.fields import RichTextField


# зарегистрированные пользователи
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


# категории объявлений
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# объявления зарегистрированных пользователей
class Ad(models.Model):
    title = models.TextField()
    description = models.TextField()
    content = RichTextUploadingField()
    published_date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='AdCategory')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])


# many-to-many между категориями и объявлениями
class AdCategory(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


# отклики на объявления
class Reply(models.Model):
    STATUS = [
        ('unknown', 'на рассмотрении'),
        ('accepted', 'принято'),
        ('rejected', 'отклонено'),
    ]

    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)

    status = models.CharField(choices=STATUS, default='unknown', max_length=255)

    def __str__(self):
        return self.status

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.ad_id)])


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='AdCategory',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )