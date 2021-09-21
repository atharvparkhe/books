# Generated by Django 3.2.7 on 2021-09-21 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0005_transactionsmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionsmodel',
            name='amt',
        ),
        migrations.AddField(
            model_name='transactionsmodel',
            name='book',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='books_transacted', to='app_main.bookmodel'),
            preserve_default=False,
        ),
    ]