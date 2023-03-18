from django.urls import path
from news.views import *
from accounts.views import *
from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path('list',list1)
]
