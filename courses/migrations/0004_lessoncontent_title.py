# Generated by Django 3.0.8 on 2020-07-11 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20200709_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessoncontent',
            name='title',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
