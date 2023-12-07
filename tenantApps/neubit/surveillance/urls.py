from django.urls import path

from tenantApps.neubit.surveillance.views import testAlert

app_name = "Surveillance"

urlpatterns = [
	# Test Alerts Config URLS
	path('test-alert/config/', testAlert.testAlert, name="test-alert-list"),
	path('testAlertCreate/', testAlert.testAlertCreate, name="test-alert-create"),
	path('testAlertUpdate/<str:pk>/', testAlert.testAlertUpdate, name="test-alert-update"),
	path('testAlertDelete/<str:pk>/', testAlert.testAlertDelete, name="test-alert-delete"),
	# Generate Alert
	path('ajax/AlertGenerate/', testAlert.generateAlert, name="generateAlert"),
	# # Alert Acknowledge & History
	path('test-alert/list/', testAlert.testAlertAckList, name="test-alert-ack-list"),
	path('testAlertAcknowledge/<str:pk>', testAlert.testAlertAcknowledge, name="testAlertAcknowledge"),
	path('testAlertsHistory/', testAlert.testAlertHistory, name="testAlertsHistory")

]
