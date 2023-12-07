import uuid

from django.db import models

from tenantApps.common.branch.models import Branch


# Create your models here.

# Demo Alerts
class TestAlert(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
	alertCode = models.CharField(max_length=20)
	alertName = models.CharField(max_length=20)
	colorCode = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.alertCode

	class Meta:
		verbose_name_plural = "Test Alert"


class TestAlertAcknowledge(models.Model):
	type_of_alert = (('False Alert', 'False Alert'),
	                 ('Genuine Alert', 'Genuine Alert'))
	status_of_alert = (
		('Pending', 'Pending'),
		('Open', 'Open'),
		('Close', 'Close')
	)
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	alert = models.ForeignKey(TestAlert, on_delete=models.CASCADE, related_name="TestAck")
	alertType = models.CharField(choices=type_of_alert, max_length=30, null=True, blank=True)
	description = models.CharField(max_length=300, null=True, blank=True)
	ack = models.CharField(choices=status_of_alert, max_length=30, null=True, blank=True, default="Pending")
	ack_status = models.BooleanField(default=False, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.alert.alertName

	class Meta:
		verbose_name_plural = "Test Alert Acknowledged"
