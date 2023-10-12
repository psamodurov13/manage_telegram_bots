from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


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
    list_editable = ('count', 'default_next_integer', 'timer', 'time', )
    search_fields = ('count', 'text', 'buttons')
    list_filter = ('bot', 'post_type')

    class Media:
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

