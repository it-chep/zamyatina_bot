from django.contrib import admin

from tg_bot.models import TgBot


class TgBotAdmin(admin.ModelAdmin):
    list_display = ('id', 'tg_id', 'username')


admin.site.register(TgBot, TgBotAdmin)
