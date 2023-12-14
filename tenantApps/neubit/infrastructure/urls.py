from django.urls import path

from tenantApps.neubit.infrastructure.views import panel, nvr, camera, iot

app_name = 'Infrastructure'

urlpatterns = [
	# path('deviceLoc/', views.deviceLoc, name='deviceLoc'),

	# Panel URLs
	path('devicePanelInfo/', panel.devicePanelInfo, name='devicePanelInfo'),
	path('devicePanelAdd/', panel.devicePanelAdd, name='devicePanelAdd'),
	path('devicePanelInfo/<str:pk>/update/', panel.devicePanelUpdate, name='devicePanelUpdate'),
	path('devicePanelInfo/<str:pk>/delete/', panel.devicePanelDelete, name='devicePanelDelete'),

	# NVR URLs
	path('deviceNvrInfo/', nvr.deviceNvrInfo, name='deviceNvrInfo'),
	path('deviceNvrAdd/', nvr.deviceNvrAdd, name='deviceNvrAdd'),
	path('deviceNvrInfo-/<str:pk>/update/', nvr.deviceNvrUpdate, name='deviceNvrUpdate'),
	path('deviceNvrInfo-/<str:pk>/delete/', nvr.deviceNvrDelete, name='deviceNvrDelete'),
	path('device/<str:pk>/detail/', nvr.nvrDetails, name='nvrDetails'),
	path('nvr/bulkUpload/', nvr.bulkUpload, name='bulkUpload'),

	# CCTV URLs
	path('device/<str:nvrId>/camera/', camera.cctvCreate, name='cctvCreate'),
	path('device/<str:nvrId>/camera/<str:cctvId>/update/', camera.cctvUpdate, name='cctvUpdate'),
	path('device/<str:nvrId>/camera/<str:cctvId>/delete/', camera.cctvDelete, name='cctvDelete'),

	# Stream Start & Stop
	path('stream/<str:nvrId>/push/<str:cctvId>/', camera.pushRtspAndStart, name='pushRtspAndStart'),
	# Recording Start & Stop
	path('stream/<str:nvrId>/record/<str:cctvId>/', camera.recordingStartAndStop, name='recordingStartAndStop'),

	# Single Camera Stream
	path('stream/<str:nvrId>/stream/<str:cctvId>/', camera.streamCamera, name='streamCamera'),

	# Camera Tag Urls
	path('tags/', camera.tagAll, name="allTag"),
	path('tags-add/', camera.tagAdd, name="addTag"),
	path('tags-delete/<str:pk>', camera.tagDelete, name="deleteTag"),
	path('tags-update/<str:pk>', camera.tagUpdate, name="updateTag"),

	# Fetch VODs
	path('vod/<str:nvrId>/fetch/', camera.fetch_and_save_vod_data, name='fetch_and_save_vod_data'),
	path('vodStream/<str:nvrId>/stream/<str:cctvId>/', camera.streamVod, name='streamVod'),

	# IOT Gateway
	path('gateway/list/', iot.iotGatewayList, name='iotGatewayList'),
	path('gateway/iot/', iot.iotGatewayCreate, name='iotGatewayCreate'),
	path('gateway/<str:iotId>/update/', iot.iotGatewayUpdate, name='iotGatewayUpdate'),
	path('gateway/<str:iotId>/delete/', iot.iotGatewayDelete, name='iotGatewayDelete'),

	# IOT Devices
	path('devices/list/', iot.iotDeviceList, name='iotDeviceList'),
	path('device/devices/', iot.iotDeviceCreate, name='iotDeviceCreate'),
	path('device/<str:deviceId>/update/', iot.iotDeviceUpdate, name='iotDeviceUpdate'),
	path('device/<str:deviceId>/delete/', iot.iotDeviceDelete, name='iotDeviceDelete'),
]
