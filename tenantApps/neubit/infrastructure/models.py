import uuid

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from guardian.shortcuts import assign_perm

from tenantApps.common.branch.models import Branch


class CameraTag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    tagName = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='tagUser', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tagName

    class Meta:
        verbose_name_plural = "Camera Tags"
        permissions = [
            ("view_tag", "Can assign camera tag"),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.ensure_view_tag_permission_exists()
        for user in self.users.all():
            assign_perm('view_tag', user, self)

    @staticmethod
    def ensure_view_tag_permission_exists():
        content_type = ContentType.objects.get_for_model(CameraTag)
        permission_codename = 'view_tag'
        try:
            permission = content_type.permission_set.get(codename=permission_codename)
        except ObjectDoesNotExist:
            from django.contrib.auth.models import Permission
            permission = Permission.objects.create(
                codename=permission_codename,
                name="Can assign camera tag",
                content_type=content_type,
            )


# Create your models here.
class Panel(models.Model):
    manufacturerChoices = (
        ("Texecom", "Texecom"),
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    selectBranch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="branchPanel")
    selectManufacturer = models.CharField(choices=manufacturerChoices, max_length=100)
    slugName = models.CharField(max_length=30)
    deviceID = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    password = models.CharField(max_length=30, null=True, blank=True)
    ipAddress = models.CharField(max_length=30)
    port = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.deviceID

    class Meta:
        verbose_name_plural = "Panel"


class NVR(models.Model):
    manufacturerChoices = (
        ("Hikvision", "Hikvision"),
        ("Octocam", "Octocam"),
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    selectBranch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="branchNvr")
    selectManufacturer = models.CharField(choices=manufacturerChoices, max_length=100)
    slugName = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    ipAddress = models.CharField(max_length=100)
    port = models.IntegerField()
    playbackUrl = models.CharField(max_length=100, null=True, blank=True)
    # status = models.BooleanField(default=False)
    # deviceID = models.CharField(max_length=200, null=True, blank=True)
    # macAddress = models.CharField(max_length=200, null=True, blank=True)
    # modelNo = models.CharField(max_length=100, null=True, blank=True)
    # hddCapacity = models.JSONField(default=dict)
    # freeHdd = models.JSONField(default=dict)
    # hddType = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slugName + " " + self.selectManufacturer

    class Meta:
        verbose_name_plural = "NVR"


class CCTV(models.Model):
    manufacturerChoices = (
        ("Hikvision", "Hikvision"),
        ("Milesight", "Milesight"),
        ("Octocam", "Octocam"),
        ("CP-Plus", "CP-Plus"),
        ("Dahua", "Dahua"),
        ("Axis", "Axis"),
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    selectNvr = models.ForeignKey(NVR, on_delete=models.CASCADE, related_name="nvr_cctv")
    selectManufacturer = models.CharField(choices=manufacturerChoices, max_length=100)
    selectTag = models.ForeignKey(CameraTag, on_delete=models.CASCADE, related_name="TaggedCCTV")
    slugName = models.CharField(max_length=30)
    deviceID = models.CharField(max_length=30)
    rtspLink = models.CharField(max_length=100, null=True, blank=True)
    hlsLink = models.CharField(max_length=100, null=True, blank=True)
    hlsCreated = models.BooleanField(default=False, null=True, blank=True)
    recordingStatus = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slugName + " " + self.deviceID

    class Meta:
        verbose_name_plural = "CCTV"


class VOD(models.Model):
    cctv = models.ForeignKey(CCTV, on_delete=models.CASCADE, related_name='vod')  # ForeignKey to CCTV
    stream_id = models.CharField(max_length=500)
    creation_date = models.BigIntegerField()
    start_time = models.BigIntegerField()
    duration = models.BigIntegerField()
    file_size = models.BigIntegerField()
    vod_id = models.CharField(max_length=500, unique=True)
    file_path = models.CharField(max_length=500, unique=True, default='No Path')

    def __str__(self):
        return self.vod_id

    class Meta:
        verbose_name_plural = "CCTV VODs"


class IotGateway(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    selectBranch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="branchIOTConfig", null=True,
                                     blank=True)
    gatewayName = models.CharField(max_length=100, null=True, blank=True)
    gatewayIp = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    fetchDevice = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.gatewayName

    class Meta:
        verbose_name_plural = "IOT Gateway"


class IotDevice(models.Model):
    sensorChoices = (
        ("Environment", "Environment"),
        ("Controller", "Controller"),
        ('Security', 'Security'),
        ('HVAC', 'HVAC'),
        ('Smart Spaces', 'Smart Spaces'),
        ('Energy', 'Energy')
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    selectBranch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="branchIOT", null=True, blank=True)
    selectGateway = models.ForeignKey(IotGateway, on_delete=models.CASCADE, related_name="gatewayIOT", null=True,
                                      blank=True)
    selectSensor = models.CharField(choices=sensorChoices, max_length=100, default="Controller", null=True, blank=True)
    devEUI = models.CharField(max_length=200, unique=True)
    selectTag = models.ForeignKey(CameraTag, on_delete=models.CASCADE, related_name="TaggedIOT", null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " " + self.description

    class Meta:
        verbose_name_plural = "IOT Device"
