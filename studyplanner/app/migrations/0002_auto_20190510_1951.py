# Generated by Django 2.1.7 on 2019-05-10 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='type_a',
            field=models.CharField(choices=[('EX', 'Exam'), ('CW', 'Coursework')], max_length=11),
        ),
    ]
