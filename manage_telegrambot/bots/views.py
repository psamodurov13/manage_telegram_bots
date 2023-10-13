from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from loguru import logger
from .models import *
from django.contrib.auth.decorators import login_required


@login_required
def index_view(request):
    context = {
        'title': 'Сводная таблица по ботам'
    }
    all_bots = Bot.objects.all()
    logger.info(f'ALL BOTS - {all_bots}')
    bots = []
    # all_tags = Tags.objects.all()
    all_mailings = Mailings.objects.all()
    for bot in all_bots:
        posts = Post.objects.filter(bot=bot)
        all_tags = []
        for post in posts:
            tags_from_post = post.add_tags.all()
            all_tags.extend(tags_from_post)
        all_tags = list(set(all_tags))
        logger.info(f'----------------------')
        logger.info(f'COLLECT DATA FOR {bot}')
        logger.info(f'ALL TAGS - {all_tags}')
        current_step_bot_subscribers_id = CurrentSteps.objects.filter(bot=bot)
        logger.info(f'current_step_bot_subscribers_id - {current_step_bot_subscribers_id}')
        subscribers = Subscribers.objects.filter(id__in=[i.subscriber.id for i in current_step_bot_subscribers_id])
        completed_current_step_bot_subscribers = current_step_bot_subscribers_id.filter(is_completed=True)
        completed_subscribers = Subscribers.objects.filter(id__in=[i.subscriber.id for i in completed_current_step_bot_subscribers])
        logger.info(f'subscribers - {subscribers}')
        tags = []
        for tag in all_tags:

            logger.info(f'TAG INFO {tag}')
            subscribers_with_tag = subscribers.filter(tags=tag)
            logger.info(f'subscribers_with_tag {subscribers_with_tag}')
            logger.info(f'COUNT SUBSCRIBERS WITH TAG {len(subscribers_with_tag)}')
            tags.append({'info': tag, 'subscribers_with_tag': subscribers_with_tag})
        mailings = []
        for mailing in all_mailings.filter(bot=bot):
            total = MailingDelivery.objects.filter(mailing=mailing).count
            delivered = MailingDelivery.objects.filter(mailing=mailing, result=True).count
            mailings.append({'info': mailing, 'delivered': delivered, 'total': total})
        bots.append({
            'info': bot,
            'subscribers': len(subscribers),
            'completed_subscribers': len(completed_subscribers),
            'active_subscribers': len(subscribers) - len(completed_subscribers),
            'tags': tags,
            'mailings': mailings
        })
    context['bots'] = bots
    return render(request, 'bots/index.html', context)


@login_required
def subscribers_view(request, bot_id):
    bot = Bot.objects.get(id=bot_id)
    current_step_bot_subscribers_id = CurrentSteps.objects.filter(bot=bot)
    logger.info(f'current_step_bot_subscribers_id - {current_step_bot_subscribers_id}')
    subscribers = Subscribers.objects.filter(id__in=[i.subscriber.id for i in current_step_bot_subscribers_id])
    subscribers_data = []
    for subscriber in subscribers:
        current_step = subscriber.current_steps.get(bot=bot)
        subscribers_data.append({
            'info': subscriber,
            'current_step': current_step
        })
    context = {
        'title': f'Подписчики бота "{bot.name} ({bot.username})"',
        'subscribers': subscribers_data,
    }
    return render(request, 'bots/subscribers.html', context)


@login_required
def mailings_view(request, bot_id):
    bot = Bot.objects.get(id=bot_id)
    all_mailings = Mailings.objects.filter(bot=bot)
    mailings = []
    for mailing in all_mailings:
        total = MailingDelivery.objects.filter(mailing=mailing).count
        delivered = MailingDelivery.objects.filter(mailing=mailing, result=True).count
        mailings.append({'info': mailing, 'delivered': delivered, 'total': total})
    context = {
        'title': f'Рассылки бота "{bot.name} ({bot.username})"',
        'mailings': mailings
    }
    return render(request, 'bots/mailings.html', context)


@login_required
def tags_view(request, bot_id):
    bot = Bot.objects.get(id=bot_id)
    all_tags = Tags.objects.all()
    tags = []
    current_step_bot_subscribers_id = CurrentSteps.objects.filter(bot=bot)
    subscribers = Subscribers.objects.filter(id__in=[i.subscriber.id for i in current_step_bot_subscribers_id])
    for tag in all_tags:
        logger.info(f'TAG INFO {tag}')
        subscribers_with_tag = subscribers.filter(tags=tag)
        tags.append({'info': tag, 'subscribers_with_tag': subscribers_with_tag})
    context = {
        'title': f'Теги бота "{bot.name} ({bot.username})"',
        'tags': tags
    }
    return render(request, 'bots/tags.html', context)


def restart_bots(request):
    result = rq.get(f'{API_URL}restart/{API_TOKEN}')
    logger.info(f'REQUEST RESULT API - {result}')
    logger.info(f'REQUEST RESULT API - {result.text}')
    messages.success(request, 'Боты перезапущены')
    return redirect('index')




