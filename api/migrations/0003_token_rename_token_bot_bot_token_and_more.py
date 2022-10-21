# Generated by Django 4.0.4 on 2022-06-04 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_customuser_bots'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameField(
            model_name='bot',
            old_name='token',
            new_name='bot_token',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='bots',
            field=models.ManyToManyField(blank=True, help_text='Bots edit field.', to='api.bot'),
        ),
    ]
