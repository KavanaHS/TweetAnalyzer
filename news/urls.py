from django.urls import path
from news.views import *
from . import views

urlpatterns = [
    path("extract", views.extract, name="extract"),
    path("index", views.index, name="index"),
    path("submit",submit),
    path('smtp_sendmail',smtp_sendmail),
  
   
    
    
   ]
