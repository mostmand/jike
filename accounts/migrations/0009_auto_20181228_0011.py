# Generated by Django 2.1.4 on 2018-12-28 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20181228_0005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersip',
            name='session',
        ),
        migrations.AddField(
            model_name='usersip',
            name='session_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
