from django.urls import path, include

from .views import branchAi, videoAi

app_name = 'Marketplace'

urlpatterns = [
	# Marketplace URLS
	path('list/', videoAi.marketplace, name="marketplace"),
	# Marketplace File Manager
	path('file/<str:modelId>/manager/', videoAi.marketplace_files_list, name='marketplace_files_list'),
	path('<str:modelId>/file-manager/upload/', videoAi.marketplace_files_create, name='marketplace_files_create'),
	path('<str:modelId>/manager/<uuid:pk>/update/', videoAi.marketplace_files_update, name='marketplace_files_update'),
	path('<str:modelId>/manager/<uuid:pk>/delete/', videoAi.marketplace_files_delete, name='marketplace_files_delete'),
	# Video Inference
	path('<str:fileId>/inference/<str:modelId>/', videoAi.streamingInference, name='streamingInference'),
	# Branch URLs
	path('asset/', branchAi.branch_list, name="branch"),
	path('<str:id>/detail/', branchAi.branch_detail, name="branch_detail"),
	# Assets URLs
	path('<str:branchId>/asset/create/', branchAi.branch_asset_create, name="branch_asset_create"),
	path('<str:branchId>/asset/<str:assetId>/update/', branchAi.branch_asset_update, name="branch_asset_update"),
	path('<str:branchId>/asset/<str:assetId>/delete/', branchAi.branch_asset_delete, name="branch_asset_delete"),
	# Branch Inference URLs
	path('<str:branchId>/asset/<str:assetId>/inference', branchAi.branch_live_inferences, name="branch_live_inferences"),
	# Inferences URLs
	# path('<str:branchId>/asset/<str:assetId>/inference/<str:modelId>/liveStream/', branchAi.live_inferences,
	#      name="branch_inference"),
	## API URLs
	path('api/', include('tenantApps.clarify.marketplace.api.api_urls'))
]
