from django.contrib import admin

# Register your models here.
from .models import TestAlert, TestAlertAcknowledge

admin.site.register(TestAlert)
admin.site.register(TestAlertAcknowledge)
