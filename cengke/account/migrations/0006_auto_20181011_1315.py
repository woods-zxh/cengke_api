# Generated by Django 2.0.4 on 2018-10-11 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20180517_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='nuser',
            name='art',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='nuser',
            name='communication',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='nuser',
            name='internation',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='nuser',
            name='leader',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='nuser',
            name='logic',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='nuser',
            name='others',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='nuser',
            name='science',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='nuser',
            name='society',
            field=models.FloatField(default=0.0),
        ),
    ]