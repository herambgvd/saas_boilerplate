from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from public.home.views import custom_404, custom_500

urlpatterns = [
	path('admin/', admin.site.urls),
	# path("__debug__/", include("debug_toolbar.urls")),
	path('', include('public.home.urls')),
	path('accounts/', include('allauth.urls')),
]

handler404 = custom_404
handler500 = custom_500

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
