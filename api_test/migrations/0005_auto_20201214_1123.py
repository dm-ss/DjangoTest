# Generated by Django 3.1.4 on 2020-12-14 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0004_auto_20201214_1121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lyzd_interface',
            old_name='Project_id',
            new_name='Project',
        ),
    ]
