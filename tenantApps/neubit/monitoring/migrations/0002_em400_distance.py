# Generated by Django 4.2.7 on 2023-12-21 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='em400',
            name='distance',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
    ]