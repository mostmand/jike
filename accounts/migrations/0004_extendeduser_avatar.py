# Generated by Django 2.1.4 on 2018-12-21 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20181221_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendeduser',
            name='avatar',
            field=models.ImageField(null=True, upload_to='media/accounts/images'),
        ),
    ]
