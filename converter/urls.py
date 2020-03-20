from django.urls import path

from . import views

app_name = 'converter'
urlpatterns = [
    path('', views.index, name='index'),
    path('convert/', views.convert, name='convert'),
    path('update-currencies/', views.update_currencies, 
	     name='update_currencies'),
    path('admin/converter/currency/<int:new>/<int:updated>/<int:removed>', 
    	 views.admin_currencies_list, 
    	 name='admin-currencies-list'),
]