# Generated by Django 3.2.7 on 2021-09-23 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0004_voting'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmodel',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
    ]
