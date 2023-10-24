from django.urls import path
from searchpaper import views

urlpatterns = [
    path('', views.search, name='search'),
]