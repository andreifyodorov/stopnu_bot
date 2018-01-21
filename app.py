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
stat = dict()

@app.route('/' + settings.TOKEN, methods=['POST'])
def webhook():
    update = telegram.update.Update.de_json(request.get_json(force=True), bot)
    process_message(
        text=update.message.text,
        chatkey=update.message.chat_id,
        send_callback=lambda text: bot.sendMessage(chat_id=update.message.chat_id, text=text)
    )

    return 'OK'


def process_message(text, chatkey, send_callback):
    if 'help' in text:
        send_callback('words I understand are "help" and "stat"')
    elif 'stat' in text:
        send_callback('I sent you %s ahas' % stat.get(chatkey, 0))
    else:
        send_callback('aha')
        stat[chatkey] = stat.get(chatkey, 0) + 1
