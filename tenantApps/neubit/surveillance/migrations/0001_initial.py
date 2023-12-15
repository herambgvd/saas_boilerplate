# Generated by Django 4.2.7 on 2023-12-15 05:29

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestAlert',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('alertCode', models.CharField(max_length=20)),
                ('alertName', models.CharField(max_length=20)),
                ('colorCode', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branch.branch')),
            ],
            options={
                'verbose_name_plural': 'Test Alert',
            },
        ),
        migrations.CreateModel(
            name='TestAlertAcknowledge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('alertType', models.CharField(blank=True, choices=[('False Alert', 'False Alert'), ('Genuine Alert', 'Genuine Alert')], max_length=30, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('ack', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Open', 'Open'), ('Close', 'Close')], default='Pending', max_length=30, null=True)),
                ('ack_status', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('alert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TestAck', to='surveillance.testalert')),
            ],
            options={
                'verbose_name_plural': 'Test Alert Acknowledged',
            },
        ),
    ]
