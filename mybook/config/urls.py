from django.contrib import admin
from django.urls import path, include
from book.views import base_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('book.urls')),
    path('common/', include('common.urls')),
    path('', base_views.index, name='index'),
]
