from django.urls import path
from . import views

app_name = 'game1'

urlpatterns = [
    path('game1', views.game_view, name='game1'),
    path('', views.game_page, name='game_page'),
    path('result/', views.result_view, name='result'),
]
