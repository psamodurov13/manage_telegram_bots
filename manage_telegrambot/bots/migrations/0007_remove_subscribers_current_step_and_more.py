# Generated by Django 4.2.5 on 2023-10-08 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0006_bot_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscribers',
            name='current_step',
        ),
        migrations.AddField(
            model_name='currentsteps',
            name='subscriber',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bots.subscribers', verbose_name='Подписчик'),
            preserve_default=False,
        ),
    ]