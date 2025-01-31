from . import views

urlpatterns = [
    path('', views.index, name='home.index'),
]