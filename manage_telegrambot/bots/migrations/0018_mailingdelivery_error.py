# Generated by Django 4.2.5 on 2023-10-12 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0017_mailingdelivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingdelivery',
            name='error',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ошибка'),
        ),
    ]
