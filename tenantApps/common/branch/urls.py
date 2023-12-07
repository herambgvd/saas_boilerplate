from django.urls import path

from . import views

app_name = 'Branch'
urlpatterns = [
	# Branch URLS
	path('', views.branch_list, name="branch"),
	path('create/', views.branch_create, name="branch_create"),
	path('<str:id>/update/', views.branch_update, name="branch_update"),
	path('<str:id>/delete/', views.branch_delete, name="branch_delete"),
	# path('<str:id>/detail/', views.branch_detail, name="branch_detail")
	path('license/', views.licenseSetting, name='license'),
]
