from django import forms

from .models import Ad, Reply


# создание объявления
class AdForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок объявления', max_length=75)
    description = forms.CharField(label='Краткое описание', max_length=125, widget=forms.Textarea)

    class Meta:
        model = Ad
        fields = [
            'title',
            'description',
            'content',
            'category',
        ]


# создание отклика
class ReplyForm(forms.ModelForm):
    content = forms.CharField(label='Напишите его здесь:', max_length=225, widget=forms.Textarea)

    class Meta:
        model = Reply
        fields = [
            'content',
        ]