# Generated by Django 4.2.7 on 2023-12-13 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network_automation', '0002_device_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='config',
            field=models.CharField(default='default', max_length=255),
        ),
    ]
