# Generated by Django 4.2.7 on 2023-12-07 11:35

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('infrastructure', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AM319',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('co2', models.IntegerField(blank=True, null=True)),
                ('hcho', models.FloatField(blank=True, null=True)),
                ('humidity', models.FloatField(blank=True, null=True)),
                ('light_level', models.IntegerField(blank=True, null=True)),
                ('pir_trigger', models.IntegerField(blank=True, null=True)),
                ('pm10', models.IntegerField(blank=True, null=True)),
                ('pm2_5', models.IntegerField(blank=True, null=True)),
                ('pressure', models.FloatField(blank=True, null=True)),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('tvoc', models.FloatField(blank=True, null=True)),
                ('buzzer_status', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('selectIOT', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='am319History', to='infrastructure.iotdevice')),
            ],
            options={
                'verbose_name_plural': 'Environment Sensor',
            },
        ),
    ]