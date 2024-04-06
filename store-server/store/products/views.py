from django.contrib.auth.context_processors import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef

from .models import Ad, Author, Category, Reply
from .forms import AdForm, ReplyForm
from .filters import AdFilter, ReplyFilter
from .models import Subscription, AdCategory

# основная страница - список объявлений
class AdList(ListView):
    model = Ad
    ordering = '-published_date'
    template_name = 'ads_list.html'
    context_object_name = 'ads_list'
    paginate_by = 2


# поиск по объявлениям
class SearchAd(ListView):
    model = Ad
    ordering = '-published_date'
    template_name = 'search_ads.html'
    context_object_name = 'search_ads'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


# список объявлений пользователя

class MyAdsList(LoginRequiredMixin, ListView):
    model = Ad
    ordering = '-published_date'
    template_name = 'my_ads.html'
    context_object_name = 'my_ads'
    paginate_by = 20

    def get_queryset(self):
        author = Author.objects.get(user=self.request.user)
        return Ad.objects.filter(author=author)


# список откликов на объявления пользователя

class ReplyAdList(LoginRequiredMixin, ListView):
    model = Reply
    ordering = '-published_date'
    template_name = 'my_ads_reply_list.html'
    context_object_name = 'my_ads_reply_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = Author.objects.get(user=self.request.user)
        self.filterset = ReplyFilter(self.request.GET, queryset, user=user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


# список откликов текущего пользователя

class MyReplyList(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Reply
    ordering = '-published_date'
    template_name = 'my_reply.html'
    context_object_name = 'my_reply'

    def get_queryset(self):
        user = self.request.user
        return Reply.objects.filter(user=user)


# список категорий
class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'category_list'


# список объявлений выбранной категории
def show_category(request, pk):
    category = Category.objects.filter(pk=pk)
    ads = Ad.objects.filter(category=pk)
    return render(request, 'category_ads.html', {'category_ads': ads, 'category': category})


# страница одного выбранного объявления
class AdDetail(DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad_detail'
    reply_form = ReplyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['replies'] = Reply.objects.filter(ad__id=self.object.pk).order_by('-published_date')
        context['reply_form'] = self.reply_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        form.save(commit=False)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ad_detail', kwargs={'pk': self.object.pk})


# ссылка на выбранный отклик
class ReplyDetail(LoginRequiredMixin, DetailView):
    raise_exception = True
    model = Reply
    template_name = 'reply_detail.html'
    context_object_name = 'reply_detail'


# создание объявления
class AdCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = AdForm
    model = Ad
    template_name = 'ad_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ad_detail', kwargs={'pk': self.object.pk})


# изменение объявления
class AdUpdate(LoginRequiredMixin, UpdateView):
    raise_exception = True
    form_class = AdForm
    model = Ad
    template_name = 'ad_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


# удаление объявления
class AdDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = Ad
    template_name = 'ad_delete.html'
    context_object_name = 'ad_delete'
    success_url = reverse_lazy('my_ads')


# создание отклика
class ReplyCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = ReplyForm
    model = Reply
    template_name = 'ad_detail.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.ad = Ad.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)


# принять отклик
@login_required
def confirm_reply(request, pk):
    reply = get_object_or_404(Reply, id=pk)

    reply.status = 'accepted'
    reply.save()

    return redirect('my_ads_reply_list')


# отклонить отклик
@login_required
def reject_reply(request, pk):
    reply = get_object_or_404(Reply, id=pk)

    reply.status = 'rejected'
    reply.save()

    return redirect('my_ads_reply_list')



def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'registration/subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
