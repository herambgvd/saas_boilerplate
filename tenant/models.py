import uuid

from django.db import models
from django_tenants.models import DomainMixin, TenantMixin


# Create your models here.
class Client(TenantMixin):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True, null=True)
	mail = models.EmailField(max_length=100, null=True, blank=True)
	logo = models.ImageField(upload_to='images/', null=True, blank=True,
	                         default='images/default/gvdRaw.png')
	is_active = models.BooleanField(default=False, blank=True, null=True)
	end_subscription = models.DateField(null=True, blank=True)
	neubit = models.BooleanField(default=False, blank=True, null=True)
	clarify = models.BooleanField(default=False, blank=True, null=True)
	bms = models.BooleanField(default=False, blank=True, null=True)
	iot = models.BooleanField(default=False, blank=True, null=True)
	cloudRecording = models.BooleanField(default=False, blank=True, null=True)
	created_on = models.DateField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)
	auto_create_schema = True
	auto_drop_schema = True

	def __str__(self):
		return f"{self.schema_name}"


class Domain(DomainMixin):
	pass
