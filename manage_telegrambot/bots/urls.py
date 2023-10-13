from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('subscribers/<int:bot_id>', views.subscribers_view, name='subscribers'),
    path('mailings/<int:bot_id>', views.mailings_view, name='mailings'),
    path('tags/<int:bot_id>', views.tags_view, name='tags'),
    path('restart-bots/', views.restart_bots, name='restart_bots'),
]
