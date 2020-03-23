from django.urls import path

from . import views

app_name = 'converter'
urlpatterns = [
    path('', views.index, name='index'),
    path('convert/', views.convert, name='convert'),
    path('update-currencies/', views.update_currencies, 
	     name='update_currencies'),
    path('admin/converter/currency/', views.admin_currencies_list, 
    	 name='admin-currencies-list'),

    path('tests/<str:test_path>/', views.tests, name='qunit-tests')
]