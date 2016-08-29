from requests.exceptions import HTTPError
from telegram.ext.commandhandler import CommandHandler

from ftb.api import FlexgetRequest, get_token
from ftb.config import config
from ftb.event import event
from ftb.handlers import register_handlers


def start(bot, update):
    message = 'Welcome to Flexget Telegram Bot!\n'
    token = config.get('token')
    username = config.get('username')
    password = config.get('password')
    base_url = config.get('base_url')
    try:
        if token:
            valid = FlexgetRequest.verify_connection()
        else:
            token = get_token(base_url, username, password)
            valid = token is not None
    except HTTPError:
        valid = False
    if not valid:
        message += 'Could not verify credentials. Please check config file'
    else:
        message += 'Press /help to see available actions'
    bot.sendMessage(update.message.chat_id, text=message)


start_handler = CommandHandler('start', start)


@event('endpoint.register')
def register():
    register_handlers([start_handler])
