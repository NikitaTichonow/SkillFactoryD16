from django.urls import path

from .views import AdList, AdDetail, AdCreate, AdUpdate, AdDelete, SearchAd, MyAdsList, CategoryList, show_category, \
    ReplyAdList, ReplyDetail, ReplyCreate, confirm_reply, reject_reply, MyReplyList, subscriptions

urlpatterns = [
    path('', AdList.as_view(), name='ads_list'),  # список всех объявлений
    path('<int:pk>/', AdDetail.as_view(), name='ad_detail'),  # ссылка на выбранное объявление
    path('create/', AdCreate.as_view(), name='ad_create'),  # создание объявления
    path('<int:pk>/update/', AdUpdate.as_view(), name='ad_update'),  # изменение объявления
    path('<int:pk>/delete/', AdDelete.as_view(), name='ad_delete'),  # удаление объявления
    path('search/', SearchAd.as_view(), name='search_ads'),  # поиск объявлений по критериям
    path('my_ads/', MyAdsList.as_view(), name='my_ads'),  # список объявлений текущего пользователя
    path('category/', CategoryList.as_view(), name='category_list'),  # список категорий
    path('category/<int:pk>', show_category, name='show_cat'),  # список объявлений выбранной категории
    path('replies/', ReplyAdList.as_view(), name='my_ads_reply_list'), # список откликов на объявления текущего пользователя
    path('reply/<int:pk>/', ReplyDetail.as_view(), name='reply_detail'),  # ссылка на выбранный отклик
    path('<int:pk>/reply/create/', ReplyCreate.as_view(), name='reply_create'),  # создание отклкика
    path('reply/confirm/<int:pk>/', confirm_reply, name='confirm_reply'),  # принять отклик
    path('reply/reject/<int:pk>/', reject_reply, name='reject_reply'),  # отклонить отклик
    path('my_replies/', MyReplyList.as_view(), name='my_reply'),  # список откликов текущего пользователя
    path('subscriptions/', subscriptions, name='subscriptions'),  # Подписки

]
