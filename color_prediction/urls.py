# color_game_project/urls.py

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('game1/', include('game1.urls')),
    path('', include('common_app.urls')),
]
