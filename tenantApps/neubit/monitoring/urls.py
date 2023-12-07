from django.urls import path

from . import views

app_name = 'Monitoring'

urlpatterns = [
	# Branch Wise Live Streaming
	path('branch/liveStream/', views.branchList, name='branchList'),
	path('branch/<str:id>/liveStream', views.branchLiveStream, name='branchLiveStreaming'),

	# Tag Based Live Streaming
	path('tagList/stream/', views.tagList, name="tagListStream"),
	path('tags/<str:id>/dyanmicStreaming/', views.dynamicTagStreaming, name="dynamicStreaming")
]
