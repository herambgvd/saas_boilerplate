# Generated by Django 4.2.7 on 2023-12-07 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='logo',
            field=models.ImageField(blank=True, default='images/default/gvdRaw.png', null=True, upload_to='images/'),
        ),
    ]
