from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.urls import reverse, path
from django.utils.html import format_html


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget, label='Текст', required=False)

    class Meta:
        model = Post
        fields = '__all__'


class BaseAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True


class BotAdmin(BaseAdmin):
    list_display = ('id', 'name', 'username', 'status',)
    list_display_links = ('id', 'name')
    list_editable = ('status', )
    search_fields = ('name', 'token')
    list_filter = ('status',)


class PostTypeAdmin(BaseAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class TagsAdmin(BaseAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class ActionsAdmin(BaseAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class ButtonsAdmin(BaseAdmin):
    list_display = ('id', 'name', 'action', 'button_text', 'next_post', 'button_url')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'button_text')
    list_filter = ('action',)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.action.name == 'Ссылка':
            return ['next_post']
        elif obj and obj.action.name == 'Следующий пост':
            return ['button_url']
        return ['next_post', 'button_url']


class PostAdmin(BaseAdmin):
    form = PostAdminForm
    list_display = ('id', 'name', 'count', 'default_next_integer', 'bot', 'timer', 'time', 'post_type',)
    list_display_links = ('id', 'name')
    # list_editable = ('count', 'default_next_integer', 'timer', 'time', )
    search_fields = ('count', 'text', 'buttons')
    list_filter = ('bot', 'post_type')

    def get_urls(self):
        # метод обработки url, с подстановкой необходимой view.

        urls = super(PostAdmin, self).get_urls()
        custom_urls = [
            path('text-message/<int:obj_id>', self.admin_site.admin_view(self.send_text_message), name='post_view'), ]
        return custom_urls + urls

    def send_text_message(self, request, obj_id):
        logger.info(f'!!!!!!!! {obj_id}')
        post_obj = Post.objects.get(id=obj_id)
        post_info = {
            'name': post_obj.name,
            'text': post_obj.text if post_obj.text else None,
            'emoji': post_obj.emoji if post_obj.emoji else None,
            'photo': post_obj.photo.url if post_obj.photo else None,
            'photo2': post_obj.photo2.url if post_obj.photo2 else None,
            'photo3': post_obj.photo3.url if post_obj.photo3 else None,
            'photo4': post_obj.photo4.url if post_obj.photo4 else None,
            'photo5': post_obj.photo5.url if post_obj.photo5 else None,
            'audio': post_obj.audio.url if post_obj.audio else None,
            'video': post_obj.video.url if post_obj.video else None,
        }
        buttons = []
        if post_obj.buttons.all():
            for button in post_obj.buttons.all():
                buttons.append({
                    'name': button.name,
                    'button_text': button.button_text,
                    'action': button.action.id,
                    'button_url': button.button_url if button.button_url else None,
                    'next_post_id': button.next_post.id if button.next_post else None,
                })
        logger.info(f'BUTTONS - {buttons}')
        post_info['buttons'] = buttons
        data = {
            'post_pk': post_obj.id,
            'post_info': post_info,
            'bot_username': post_obj.bot.username,
        }
        result = rq.post(f'{API_URL}send-test-message', data=json.dumps(data), headers=headers)
        logger.info(f'RESULT - {result}')
        return redirect(request.META['HTTP_REFERER'])

    class Media:
        model = Post
        css = {
            'all': ('admin/css/custom_admin.css',),
        }


class CurrentStepsAdmin(BaseAdmin):
    list_display = ('id', 'subscriber', 'bot', 'current_step',)
    list_display_links = ('id',)
    search_fields = ('current_step',)
    list_filter = ('bot',)


class SubscribersAdmin(BaseAdmin):
    list_display = ('id', 'telegram_id', 'first_name', 'last_name', 'username',)
    list_display_links = ('id', 'telegram_id')
    search_fields = ('telegram_id', 'first_name', 'last_name', 'username',)
    list_filter = ('tags',)


class MailingsAdmin(BaseAdmin):
    list_display = ('id', 'name', 'time', 'tag', )
    list_display_links = ('id', 'name')
    search_fields = ('name', 'text', )
    list_filter = ('tag',)


admin.site.register(Bot, BotAdmin)
admin.site.register(PostType, PostTypeAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Actions, ActionsAdmin)
admin.site.register(Buttons, ButtonsAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(CurrentSteps, CurrentStepsAdmin)
admin.site.register(Subscribers, SubscribersAdmin)
admin.site.register(Mailings, MailingsAdmin)

