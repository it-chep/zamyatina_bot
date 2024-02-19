import json
import os, sys
import telebot

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.core.management.base import BaseCommand
from django.conf import settings
from tg_bot.models import TgBot

bot = telebot.TeleBot(settings.BOT_TOKEN)


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])
    return HttpResponse(status=200)


START_MESSAGE = """
Этот бот не поможет стать тебе великим рентгенологом, но кое-что он умеет.
Привет! Это бот Giftradiology от Ксении и Валерии, который поделиться с тобой полезными материалами за отметку в сториз

Пришлите, пожалуйста, в этот бот скриншот своей сторис с отметкой нашего  YouTube-канала. Я все проверю и пришлю вам дополнительные материалы:

-33 совета по развитию в рентгенологии 
-мини-лекция по КТ-семиотики образований печени
"""


class Handler:
    bot = bot

    @staticmethod
    @bot.message_handler(commands=['start'])
    def start_message(message):
        try:
            username = f"@{message.from_user.username}"
        except AttributeError:
            username = None

        TgBot.objects.get_or_create(
            tg_id=message.chat.id,
            username=username,
            name=message.from_user.first_name
        )

        bot.send_message(message.chat.id, START_MESSAGE)

    @staticmethod
    @bot.message_handler(content_types=['document', 'photo'])
    def send_thanks(message, ):
        user = TgBot.objects.filter(tg_id=message.chat.id).first()

        if user.get_bonus:
            bot.send_message(message.chat.id, 'Бонус можно получить только 1 раз')
            return

        user.get_bonus = True
        user.save()

        bot.send_message(message.chat.id, 'Супер, держи наши дополнительные материалы:')

    @staticmethod
    @bot.message_handler(commands='statistic_users')
    def statistic_users(message, ):
        bot.send_message(message.chat.id, f'Пользователей в боте: {TgBot.objects.all().count()}')

    # @staticmethod
    # @bot.message_handler(func=lambda message: True)
    # def send_some_message(message):
    #     if not (Handler.service.get_day_mood_state(message)):
    #         Handler.send_mood_notice(message)
    #         return
    #     messages, markups, photos = Handler.service.fork(message)
    #
    #     if photos:
    #         for photo_name in photos:
    #             bot.send_photo(message.chat.id, photo=open(photo_name, 'rb'))
    #
    #             if os.path.exists(photo_name) and 'NEW' in photo_name:
    #                 os.remove(os.path.join(settings.BASE_DIR, photo_name))
    #     # print(markups, messages)
    #     for markup, msg in zip(markups, messages):
    #         bot.send_message(message.chat.id, msg, reply_markup=markup)
    #     for ids in markups:
    #         if type(ids) == list:
    #             for tg_id in ids:
    #                 # print(tg_id)
    #                 bot.send_message(tg_id, message.text)
    #             bot.send_message(message.chat.id, "Рассылка завершена !")
    #
    #     Handler.service.clean_markup()
    #     Handler.service.clean_markup()
