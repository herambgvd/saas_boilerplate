from django.urls import path

from . import views

app_name = 'Staff'
urlpatterns = [
	# Group URLs
	path('group/', views.groups, name='groups'),
	path('group/create/', views.group_create, name="group_create"),
	path('group/<int:group_id>/edit/', views.group_update, name="group_update"),
	path('group/<int:group_id>/delete/', views.group_delete, name="group-delete"),
	# User URLs
	path('users/', views.user_list, name='user_list'),
	path('users/create/', views.create_user, name='create_user'),
	path('users/update/<int:user_id>/', views.update_user, name='update_user'),
	path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
