from django.db import models
from manage_telegrambot.utils import CustomStr
import requests as rq
from loguru import logger
from manage_telegrambot.config import API_TOKEN, API_URL
import json
from manage_telegrambot.config import headers
import time


class Bot(CustomStr, models.Model):
    name = models.CharField(max_length=255, verbose_name='Название бота',
                            help_text='Используется только Вами, пользователи его не видят')
    username = models.CharField(max_length=255, verbose_name='Имя бота',
                                help_text='username, использующийся для поиска в telegram')
    token = models.CharField(max_length=255, verbose_name='Token', help_text='Токен из BotFather')
    status = models.BooleanField(default=False, verbose_name='Включен')

    def save(self, *args, **kwargs):
        super(Bot, self).save(*args, **kwargs)
        result = rq.get(f'{API_URL}restart/{API_TOKEN}')
        logger.info(f'REQUEST RESULT API - {result}')
        logger.info(f'REQUEST RESULT API - {result.text}')

    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Боты'


class PostType(CustomStr, models.Model):
    name = models.CharField(max_length=255, verbose_name='Название типа')

    class Meta:
        verbose_name = 'Тип поста'
        verbose_name_plural = 'Типы постов'


class Tags(CustomStr, models.Model):
    name = models.CharField(max_length=255, verbose_name='Название тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Actions(CustomStr, models.Model):
    name = models.CharField(max_length=255, verbose_name='Название действия')

    class Meta:
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'


class Buttons(CustomStr, models.Model):
    name = models.CharField(max_length=255, verbose_name='Название кнопки', help_text='Это название видете только Вы')
    button_text = models.CharField(max_length=255, verbose_name='Текст кнопки', help_text='Введите текст, который будет отображаться внутри кнопки')
    action = models.ForeignKey(Actions, verbose_name='Действие', on_delete=models.CASCADE, related_name='buttons',
                               help_text='Для активации следующих полей нажмите кнопку "Сохранить и продолжить редактирование"')
    button_url = models.URLField(verbose_name='Ссылка', blank=True, null=True, help_text='Заполняется только при действии "переход по ссылке"')
    next_post = models.ForeignKey('Post', verbose_name='Следующий пост', on_delete=models.CASCADE, blank=True,
                                  null=True, related_name='buttons_to_post',
                                  help_text='Заполняется только при действии "переход к следующему посту"')

    class Meta:
        verbose_name = 'Кнопка'
        verbose_name_plural = 'Кнопки'


class Post(CustomStr, models.Model):
    bot = models.ForeignKey(Bot, verbose_name='Бот', on_delete=models.CASCADE, related_name='posts')
    post_type = models.ForeignKey(PostType, verbose_name='Тип поста', on_delete=models.CASCADE, related_name='posts')
    name = models.CharField(max_length=255, verbose_name='Название поста',
                            help_text='Используется только для удобства администрирования')
    text = models.TextField(verbose_name='Текст поста', blank=True, null=True, help_text='Текстовая часть сообщения')
    emoji = models.CharField(max_length=25, verbose_name='Emoji', blank=True, null=True, help_text='Emoji')
    photo = models.ImageField(verbose_name='Фото файл', upload_to='photo/', blank=True, null=True,
                             help_text='Загрузите фото файл в формате .jpg')
    photo2 = models.ImageField(verbose_name='Фото файл', upload_to='photo/', blank=True, null=True,
                              help_text='Загрузите фото файл в формате .jpg')
    photo3 = models.ImageField(verbose_name='Фото файл', upload_to='photo/', blank=True, null=True,
                              help_text='Загрузите фото файл в формате .jpg')
    photo4 = models.ImageField(verbose_name='Фото файл', upload_to='photo/', blank=True, null=True,
                              help_text='Загрузите фото файл в формате .jpg')
    photo5 = models.ImageField(verbose_name='Фото файл', upload_to='photo/', blank=True, null=True,
                              help_text='Загрузите фото файл в формате .jpg')
    audio = models.FileField(verbose_name='Аудио файл', upload_to='audio/', blank=True, null=True,
                             help_text='Загрузите аудио файл в формате .ogg')
    video = models.FileField(verbose_name='Видео файл', upload_to='video/', blank=True, null=True,
                             help_text='Загрузите видео файл в формате .mp4')
    count = models.CharField(max_length=15, verbose_name='Custom ID',
                             help_text='Идентификатор, используется для указания следующего поста')
    timer = models.IntegerField(verbose_name='Таймер', blank=True, null=True,
                                help_text='Заполняется в том случае, если данный пост должен отправляться через определенное время после предыдущего. Таймер указывается в секундах')
    time = models.TimeField(verbose_name='Время', blank=True, null=True,
                            help_text='Время отправки поста. Указывается в случае, если пост должен быть отправлен в определенное время после предыдущего поста')
    default_next_integer = models.CharField(max_length=255, verbose_name='Next ID', blank=True,
                                            null=True, help_text='Идентификатор следующего поста')
    buttons = models.ManyToManyField(Buttons, verbose_name='Кнопки', related_name='posts', blank=True)
    add_tags = models.ManyToManyField(Tags, verbose_name='Добавляемые теги', related_name='posts', blank=True,
                                      help_text='Выберите теги, которые будут добавлены пользователю после отправки данного поста')
    is_final_post = models.BooleanField(default=False, verbose_name='Последний пост воронки')


    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        unique_together = ('count', 'bot')


class Subscribers(CustomStr, models.Model):
    telegram_id = models.IntegerField(verbose_name='Telegram ID')
    first_name = models.CharField(max_length=255, verbose_name='Имя', blank=True, null=True,)
    last_name = models.CharField(max_length=255, verbose_name='Фамилия', blank=True, null=True,)
    username = models.CharField(max_length=255, verbose_name='Username', blank=True, null=True,)
    created_at = models.DateTimeField(verbose_name='Дата и время подписки', auto_now_add=True)
    tags = models.ManyToManyField(Tags, verbose_name='Теги', related_name='subscribers')
    # current_step = models.ManyToManyField(CurrentSteps, verbose_name='Текущий шаг',
    #                                       related_name='subscriber')

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'


class CurrentSteps(CustomStr, models.Model):
    subscriber = models.ForeignKey(Subscribers, verbose_name='Подписчик', on_delete=models.CASCADE,
                                   related_name='current_steps')
    bot = models.ForeignKey(Bot, verbose_name='Бот', on_delete=models.CASCADE, related_name='current_steps')
    current_step = models.CharField(max_length=255, verbose_name='Текущий шаг',
                                    help_text='Идентификатор поста, который должен быть отправлен следующим')
    is_completed = models.BooleanField(default=False, verbose_name='Воронка завершена')


    class Meta:
        verbose_name = 'Текущий шаг'
        verbose_name_plural = 'Текущие шаги'


class Mailings(CustomStr, models.Model):
    name = models.CharField(max_length=255, verbose_name='Название рассылки')
    bot = models.ForeignKey(Bot, verbose_name='Бот', on_delete=models.CASCADE, related_name='mailings')
    text = models.TextField(verbose_name='Текст рассылки', blank=True, null=True,)
    time = models.DateTimeField(verbose_name='Время и дата запуска рассылки')
    photo = models.ImageField(verbose_name='Картинка', blank=True, null=True, upload_to='mailings/')
    # audio = models.FileField(verbose_name='Аудио', blank=True, null=True, upload_to='mailings/')
    video = models.FileField(verbose_name='Видео', blank=True, null=True, upload_to='mailings/')
    tag = models.ForeignKey(Tags, verbose_name='Тег', blank=True, null=True, on_delete=models.CASCADE, related_name='mailings')
    button_text = models.CharField(verbose_name='Текст кнопки', max_length=100, blank=True, null=True)
    button_url = models.CharField(verbose_name='Ссылка', max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Mailings, self).save(*args, **kwargs)
        mailing_info = {
                    'name': self.name,
                    'text': self.text,
                    'photo': self.photo.url if self.photo else None,
                    'video': self.video.url if self.video else None,
                    'tag_id': self.tag.id if self.tag else None,
                    'bot_id': self.bot.id,
                    'button_text': self.button_text,
                    'button_url': self.button_url,
                }
        mailing_pk = self.id
        if self.tag:
            all_users_id = [i.subscriber_id for i in CurrentSteps.objects.filter(bot=self.bot)]
            logger.info(f'ALL USERS ID - {all_users_id}')
            users = [[i.telegram_id, i.id] for i in Subscribers.objects.filter(id__in=all_users_id, tags=self.tag)]
            logger.info(f'ALL USERS ID - {users}')
        else:
            users = [[i.subscriber.telegram_id, i.subscriber_id] for i in CurrentSteps.objects.filter(bot=self.bot)]
            logger.info(f'ALL USERS ID - {users}')
        logger.info(f'TIME {self.time}')
        logger.info(f'TIMESTAMP {self.time.timestamp()}')
        interval = self.time.timestamp() - time.time()
        logger.info(f'INTERVAL {interval}')
        data = {
            'mailing_pk': mailing_pk,
            'mailing_info': mailing_info,
            'interval': interval,
            'users_telegram_id_id': users,
            'bot_username': self.bot.username
        }
        logger.info(f'Mailing PK - {mailing_pk}')
        logger.info(f'Mailing INFO - {mailing_info}')
        result = rq.post(f'{API_URL}start-mailing', data=json.dumps(data), headers=headers)
        logger.info(f'RESULT - {result}')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['-id']


class MailingDelivery(CustomStr, models.Model):
    mailing = models.ForeignKey(Mailings, verbose_name='Рассылка', on_delete=models.CASCADE,
                                related_name='mailing_delivery')
    subscriber = models.ForeignKey(Subscribers, verbose_name='Подписчик', on_delete=models.CASCADE,
                                   related_name='mailing_delivery')
    result = models.BooleanField(verbose_name='Доставлено')
    error = models.CharField(verbose_name='Ошибка', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Доставка рассылки'
        verbose_name_plural = 'Доставка рассылки'

