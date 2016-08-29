from requests.exceptions import HTTPError
from telegram.ext.commandhandler import CommandHandler

from ftb.api import FlexgetRequest, get_token
from ftb.config import CONFIG
from ftb.event import event
from ftb.handler import register_handlers


def start(bot, update):
    message = 'Welcome to Flexget Telegram Bot!\n'
    try:
        if CONFIG.flexget_token:
            valid = FlexgetRequest.verify_connection()
        else:
            token = get_token(CONFIG.username, CONFIG.password)
            valid = token is not None
    except HTTPError:
        valid = False
    if not valid:
        message += 'Could not verify credentials. Please check config file'
    else:
        message += 'Press /help to see available actions'
    bot.sendMessage(update.message.chat_id, text=message)


start_handler = CommandHandler('start', start)


@event('handler.register')
def register_handler():
    register_handlers(start_handler)
