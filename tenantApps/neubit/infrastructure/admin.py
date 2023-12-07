from django.contrib import admin

# Register your models here.
from .models import CCTV, NVR, Panel, CameraTag, VOD, IotGateway, IotDevice

admin.site.register(CCTV)
admin.site.register(NVR)
admin.site.register(Panel)
admin.site.register(CameraTag)
admin.site.register(VOD)
admin.site.register(IotGateway)
admin.site.register(IotDevice)
