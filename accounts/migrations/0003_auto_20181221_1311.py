# Generated by Django 2.1.4 on 2018-12-21 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20181221_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extendeduser',
            name='id',
        ),
        migrations.AlterField(
            model_name='extendeduser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
