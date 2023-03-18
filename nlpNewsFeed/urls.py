"""nlpNewsFeed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from news.views import *



urlpatterns = [
   
    path('', include('twitter.urls')),
    path('accounts/', include('accounts.urls')),
    path('news/', include('news.urls')),
    path('news/news/',include('news.urls')),
    path('index1',index1),
    #path('percentage',percentage),
    path('main',main),
    path("submit",submit),
    path('smtp_sendmail',smtp_sendmail),
    path('send',send),
    path("index",index),
   

]
