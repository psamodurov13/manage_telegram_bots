# Generated by Django 4.2.5 on 2023-10-12 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0014_mailings_bot'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photo2',
            field=models.ImageField(blank=True, help_text='Загрузите фото файл в формате .jpg', null=True, upload_to='photo/', verbose_name='Фото файл'),
        ),
        migrations.AddField(
            model_name='post',
            name='photo3',
            field=models.ImageField(blank=True, help_text='Загрузите фото файл в формате .jpg', null=True, upload_to='photo/', verbose_name='Фото файл'),
        ),
        migrations.AddField(
            model_name='post',
            name='photo4',
            field=models.ImageField(blank=True, help_text='Загрузите фото файл в формате .jpg', null=True, upload_to='photo/', verbose_name='Фото файл'),
        ),
        migrations.AddField(
            model_name='post',
            name='photo5',
            field=models.ImageField(blank=True, help_text='Загрузите фото файл в формате .jpg', null=True, upload_to='photo/', verbose_name='Фото файл'),
        ),
    ]
