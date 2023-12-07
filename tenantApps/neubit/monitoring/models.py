import uuid

from django.db import models

from tenantApps.neubit.infrastructure.models import IotDevice


# Create your models here.

class AM319(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	selectIOT = models.ForeignKey(IotDevice, on_delete=models.CASCADE, related_name="am319History", null=True,
	                              blank=True)
	co2 = models.IntegerField(null=True, blank=True)
	hcho = models.FloatField(null=True, blank=True)
	humidity = models.FloatField(null=True, blank=True)
	light_level = models.IntegerField(null=True, blank=True)
	pir_trigger = models.IntegerField(null=True, blank=True)
	pm10 = models.IntegerField(null=True, blank=True)
	pm2_5 = models.IntegerField(null=True, blank=True)
	pressure = models.FloatField(null=True, blank=True)
	temperature = models.FloatField(null=True, blank=True)
	tvoc = models.FloatField(null=True, blank=True)
	buzzer_status = models.IntegerField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "Environment Sensor"


# class VS330(models.Model):
# 	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
# 	selectIOT = models.ForeignKey(IotDevice, on_delete=models.CASCADE, related_name="vs330History", null=True,
# 	                              blank=True)
# 	distance = models.CharField(max_length=100, null=True, blank=True)
# 	occupancy = models.CharField(max_length=100, null=True, blank=True)
# 	created_at = models.DateTimeField(auto_now_add=True)
#
# 	class Meta:
# 		verbose_name_plural = "Occupancy Sensor"
#
#
# class R718N3(models.Model):
# 	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
# 	selectIOT = models.ForeignKey(IotDevice, on_delete=models.CASCADE, related_name="r718History", null=True,
# 	                              blank=True)
# 	current1 = models.FloatField(null=True, blank=True)
# 	current2 = models.FloatField(null=True, blank=True)
# 	current3 = models.FloatField(null=True, blank=True)
# 	multiplier = models.FloatField(null=True, blank=True)
# 	volt = models.FloatField(null=True, blank=True)
# 	created_at = models.DateTimeField(auto_now_add=True)
#
# 	class Meta:
# 		verbose_name_plural = "Current Meter"
