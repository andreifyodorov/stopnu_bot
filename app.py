#!/usr/bin/env python

from os import getenv
from collections import defaultdict
from flask import Flask, request
from chatflow import Chatflow, ChatContext
import telegram
import settings

if getenv('IS_PLAYGROUND'):
    import settings_playground


bot = telegram.Bot(settings.TOKEN)
bot.setWebhook(url='https://%s/%s' % (settings.WEBHOOK_HOST, settings.TOKEN),
               certificate=open(settings.CERT, 'rb'))
# print bot.getWebhookInfo()

app = Flask(__name__)
user_context = defaultdict(ChatContext)

@app.route('/' + settings.TOKEN, methods=['POST'])
def webhook():
    update = telegram.update.Update.de_json(request.get_json(force=True), bot)

    text = update.message.text
    chatkey = update.message.chat_id

    if text is not None:
        chatflow = Chatflow(
            context=user_context[chatkey],
            reply_callback=lambda text: bot.sendMessage(chat_id=chatkey, text=text))

        chatflow.process_message(text)

    return 'OK'
