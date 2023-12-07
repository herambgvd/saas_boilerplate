from django.contrib import admin

# Register your models here.
from .models import Marketplace, MarketplaceFiles, Asset

admin.site.register(Marketplace)
admin.site.register(MarketplaceFiles)
admin.site.register(Asset)
