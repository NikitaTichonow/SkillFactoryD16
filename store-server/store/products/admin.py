from django.contrib import admin
from .models import Ad, Category, Author

admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(Author)
