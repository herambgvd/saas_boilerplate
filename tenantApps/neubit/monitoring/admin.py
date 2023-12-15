from django.contrib import admin

# Register your models here.
from .models import AM319, GS301, VS121, EM300, EM400, UC512, WS201
# VS330, R718N3
#
admin.site.register(AM319)
admin.site.register(GS301)
admin.site.register(VS121)
admin.site.register(EM300)
admin.site.register(EM400)
admin.site.register(UC512)
admin.site.register(WS201)