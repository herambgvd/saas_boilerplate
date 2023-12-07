from django.contrib import admin

# Register your models here.
from .models import Country, State, City, Branch, ConfigManager

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Branch)
admin.site.register(ConfigManager)
