import uuid

from django.core.exceptions import ValidationError
from django.db import models

from tenantApps.common.branch.models import Branch


def icon_upload_to(instance, filename):
	print(instance)
	return 'icons/{}'.format(filename)


def weights_upload_to(instance, filename):
	print(instance)
	return 'weights/{}'.format(filename)


# Create your models here.
class Marketplace(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=300, null=True, blank=True)
	icon = models.FileField(upload_to=icon_upload_to)
	weights = models.FileField(upload_to=weights_upload_to)
	no_of_usage_allowed = models.PositiveIntegerField(null=True, blank=True, default=1)
	no_of_used = models.PositiveIntegerField(null=True, blank=True, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name + ' -- ' + self.description

	class Meta:
		verbose_name_plural = "AI Model Marketplace"

	def current_usage(self):
		return Asset.objects.filter(tagModel=self).count()


class MarketplaceFiles(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	selectMarketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True, blank=True)
	fileName = models.FileField(upload_to='demoFile')
	fileSize = models.FloatField(null=True, blank=True, default=0)
	status = models.BooleanField(default=False, null=True, blank=True)
	analysedVideoUrl = models.CharField(max_length=500, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Video AI"


## Assets Models ####
class AssetManager(models.Manager):
	def create_asset(self, name, liveUrl, selectBranch, tagModel):
		for marketplace in tagModel:
			if marketplace.no_of_used >= marketplace.no_of_usage_allowed:
				raise ValidationError(f"Usage limit for {marketplace.name} has been exceeded.")
			marketplace.no_of_used += 1  # Increment the usage count
			marketplace.save()

		asset = self.create(name=name, liveUrl=liveUrl, selectBranch=selectBranch)
		asset.tagModel.set(tagModel)

		return asset


class Asset(models.Model):
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	name = models.CharField(max_length=100)
	liveUrl = models.CharField(max_length=300)
	selectBranch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='assets')
	tagModel = models.ManyToManyField(Marketplace, related_name='marketplaceTagged')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = AssetManager()

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Branch Live Inference"
