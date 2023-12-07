from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('tenant/', admin.site.urls),
	# path("__debug__/", include("debug_toolbar.urls")),
	path('accounts/', include('allauth.urls')),
	path('', include('tenantApps.common.base.urls')),
	# Common URLs
	path('branch/', include('tenantApps.common.branch.urls')),
	path('staff/', include('tenantApps.common.staff.urls')),
	# Neubit URLS
	path('infra/', include('tenantApps.neubit.infrastructure.urls')),
	path('monitoring', include('tenantApps.neubit.monitoring.urls')),
	path('surv/', include('tenantApps.neubit.surveillance.urls')),
	# Clarify URLs
	path('marketplace/', include('tenantApps.clarify.marketplace.urls')),
	path('alert/', include('tenantApps.clarify.alerts.urls')),
	# Chaining Url
	path('chaining/', include('smart_selects.urls'))
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
