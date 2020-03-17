from django.urls import path

from . import views

app_name = 'converter'
urlpatterns = [
    path('', views.index, name='index'),
    path('currencies/', views.currencies, name='list_currencies'),
    path('convert/', views.convert, name='convert')
]