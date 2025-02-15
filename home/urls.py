from django.urls import path
from . import views
urlpatterns = [
<<<<<<< HEAD
    path('index/', views.index, name='home.index'),
    path('about/', views.about, name='home.about'),
]
=======
    path('index', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
]
>>>>>>> 2d8d7379ff945c4af224060bc4b8edd596a37b39
