# Generated by Django 2.0.4 on 2018-05-07 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_auto_20180506_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='allcourses',
            name='weight',
            field=models.FloatField(default=0.0),
        ),
    ]
