from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.index, name='home.index'),
    path('about/', views.about, name='home.about'),
    path('', views.about, name='home.index'),
]