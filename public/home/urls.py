from django.urls import path

from . import views

app_name = "publicHome"

urlpatterns = [
	path('', views.dashboard, name='dashboard'),
	## Domain URL
	path('domain/', views.domainList, name='domainList'),
	path('domain/create_domain/', views.createDomain, name='createDomain'),
	## Tenant URLs
	path('tenant/', views.tenantList, name='tenantList'),
	path('tenant/create/', views.createTenant, name='createTenant'),
	path('tenant/<str:tenantId>/delete/', views.deleteTenant, name='deleteTenant')
]
