# Generated by Django 2.1.7 on 2019-03-29 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20190329_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assessment',
            name='progress',
        ),
    ]