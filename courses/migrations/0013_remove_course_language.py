# Generated by Django 3.0.8 on 2020-07-30 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20200728_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='language',
        ),
    ]
