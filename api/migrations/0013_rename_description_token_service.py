# Generated by Django 4.0.4 on 2022-06-08 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='token',
            old_name='description',
            new_name='service',
        ),
    ]
