#!/usr/bin/env python

from os import getenv
from random import choice
from flask import Flask, request
import telegram
import settings

if getenv('IS_PLAYGROUND'):
    import settings_playground


bot = telegram.Bot(settings.TOKEN)
bot.setWebhook(url='https://%s/%s' % (settings.WEBHOOK_HOST, settings.TOKEN),
               certificate=open(settings.CERT, 'rb'))
# print bot.getWebhookInfo()

app = Flask(__name__)


REPLIES = ['Go away', 'Get lost', 'Screw you', 'Leave me alone']


@app.route('/' + settings.TOKEN, methods=['POST'])
def webhook():
    update = telegram.update.Update.de_json(request.get_json(force=True), bot)
    bot.sendMessage(chat_id=update.message.chat_id, text=choice(REPLIES))

    return 'OK'