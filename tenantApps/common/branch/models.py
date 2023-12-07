import uuid

from django.contrib.auth.models import User
from django.db import models
from guardian.shortcuts import assign_perm
# Create your models here.
from smart_selects.db_fields import ChainedForeignKey


# Create your models here.
class Country(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	name = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Country"


class State(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
	name = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "State"


class City(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
	name = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "City"


class Branch(models.Model):
	regionNameChoice = (
		('North', 'North Zone'),
		('East', 'East Zone'),
		('West', 'West Zone'),
		('South', 'South Zone')
	)
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	regionName = models.CharField(max_length=10, choices=regionNameChoice)
	country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='branches')
	state = ChainedForeignKey(State,
	                          chained_field="country",
	                          related_name='branches',
	                          chained_model_field="country",
	                          show_all=False,
	                          auto_choose=True,
	                          sort=True,
	                          on_delete=models.SET_NULL,
	                          null=True
	                          )
	city = ChainedForeignKey(City,
	                         chained_field="state", related_name='branches',
	                         chained_model_field="state",
	                         show_all=False,
	                         auto_choose=True,
	                         sort=True,
	                         on_delete=models.SET_NULL,
	                         null=True
	                         )
	branchCode = models.CharField(max_length=10, null=True)
	branchName = models.CharField(max_length=100, null=True)
	branchAddress = models.CharField(max_length=100, null=True)
	status = models.BooleanField(default=True)
	users = models.ManyToManyField(User, related_name='branchUser', blank=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, default='0')
	longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, default='0')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.branchName

	class Meta:
		verbose_name_plural = "Branch"

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		for user in self.users.all():
			assign_perm('view_branch', user, self)


class ConfigManager(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	configName = models.CharField(max_length=10, null=True, blank=True)
	configValue = models.CharField(max_length=200, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.configName

	class Meta:
		verbose_name_plural = "Config Manager"
