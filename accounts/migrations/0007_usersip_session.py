# Generated by Django 2.1.4 on 2018-12-28 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('accounts', '0006_usersip'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersip',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sessions.Session'),
        ),
    ]