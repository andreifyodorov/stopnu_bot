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

    text = update.message.text
    chatkey = update.message.chat_id
    if text is not None:
        process_message(
            text=text,
            chatkey=chatkey,
            send_callback=lambda text: bot.sendMessage(chat_id=chatkey, text=text)
        )

    return 'OK'


def process_message(text, chatkey, send_callback):
    tokens = text.lower().split(" ");  # tokenize

    user_stat = None
    if chatkey in stat:
        user_stat = stat[chatkey]
    else:
        user_stat = {}
        stat[chatkey] = user_stat

    if 'help' in tokens:
        send_callback('words I understand are "help" and "stat", and I will count everything else')

    elif 'stat' in tokens:
        for k, v in user_stat.iteritems():
            send_callback('You sent %d "%s"s' % (v, k))

    else:
        for token in tokens:
            v = user_stat[token] = user_stat.get(token, 0) + 1
            send_callback('It was %d "%s"s' % (v, token))
