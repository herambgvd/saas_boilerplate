from django.urls import path

from . import views
from .aiDashboardHelper import aiUtils
from .iocDashboardHelper import utils

app_name = "tenantHome"

urlpatterns = [
	path('', views.dashboard, name='dashboard'),
	path('ai/dashboard/', views.aiDashboard, name='aiDashboard'),
	path('bms/dashboard/', views.bmsDashboard, name='bmsDashboard'),
	path('iot/dashboard/', views.iotDashboard, name='iotDashboard'),

	## IOC Dashboard AJAX URLs,
	path('branch-data/', utils.branch_data, name='branch_data'),
	path('devices-per-branch-data/', utils.devices_per_branch_data, name='devices_per_branch_data'),
	path('branch-emap/', utils.get_branch_map, name='get_branch_map'),
	path('branch-demo-alerts/', utils.get_demo_alert_data, name='get_demo_alert_data'),

	## IOT Dashboard
	path('iot/branch/<str:branchId>/', views.iotBranchDashboard, name='iotBranchDashboard'),

	## AI Dashboard AJAX URLs
	path('ai-models-data/', aiUtils.ai_models_data, name='ai_models_data')
]
