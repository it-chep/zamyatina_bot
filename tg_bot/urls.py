from django.urls import include, path
from django.views.decorators.cache import cache_page
from django.conf import settings

from tg_bot.bot_handler import telegram_webhook

urlpatterns = [
    path(f'{settings.BOT_TOKEN}/', telegram_webhook, name='bot'),
]
