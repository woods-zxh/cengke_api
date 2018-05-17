# Generated by Django 2.0.4 on 2018-05-12 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_nuser_is_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nuser',
            old_name='is_post',
            new_name='can_post',
        ),
        migrations.AddField(
            model_name='nuser',
            name='term',
            field=models.CharField(default='0', max_length=20),
        ),
        migrations.AddField(
            model_name='nuser',
            name='week',
            field=models.CharField(default='0', max_length=20),
        ),
        migrations.AlterField(
            model_name='nuser',
            name='table_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
