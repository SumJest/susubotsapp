from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('keyboard/', views.keyboard, name='keyboard'),
    path('message/', views.message, name='message')
]