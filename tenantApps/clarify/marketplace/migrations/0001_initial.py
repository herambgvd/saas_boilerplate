# Generated by Django 4.2.7 on 2023-12-07 11:35

from django.db import migrations, models
import django.db.models.deletion
import tenantApps.clarify.marketplace.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marketplace',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('icon', models.FileField(upload_to=tenantApps.clarify.marketplace.models.icon_upload_to)),
                ('weights', models.FileField(upload_to=tenantApps.clarify.marketplace.models.weights_upload_to)),
                ('no_of_usage_allowed', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('no_of_used', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'AI Model Marketplace',
            },
        ),
        migrations.CreateModel(
            name='MarketplaceFiles',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('fileName', models.FileField(upload_to='demoFile')),
                ('fileSize', models.FloatField(blank=True, default=0, null=True)),
                ('status', models.BooleanField(blank=True, default=False, null=True)),
                ('analysedVideoUrl', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('selectMarketplace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.marketplace')),
            ],
            options={
                'verbose_name_plural': 'Video AI',
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('liveUrl', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('selectBranch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='branch.branch')),
                ('tagModel', models.ManyToManyField(related_name='marketplaceTagged', to='marketplace.marketplace')),
            ],
            options={
                'verbose_name_plural': 'Branch Live Inference',
            },
        ),
    ]
