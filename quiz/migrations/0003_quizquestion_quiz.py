# Generated by Django 3.0.8 on 2020-09-10 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20200910_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizquestion',
            name='quiz',
            field=models.ManyToManyField(to='quiz.Quiz'),
        ),
    ]
