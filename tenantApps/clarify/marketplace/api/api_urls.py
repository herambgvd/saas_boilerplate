from django.urls import path

from tenantApps.clarify.marketplace.api.video import views

urlpatterns = [
    path('marketplace-files/<uuid:id>/update/', views.update_marketplace_file, name='api-marketplace-files-update'),
]
