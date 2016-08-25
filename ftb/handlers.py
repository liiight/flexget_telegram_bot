import logging

from telegram.ext.commandhandler import CommandHandler
from ftb.endpoints.movie_list import main_conversation
from ftb.api import FlexgetRequest
from ftb.bot import config

logger = logging.getLogger(__name__)

HANDLERS = []
ERROR_HANDLERS = []
HELP_MESSAGE = ''


def start(bot, update):
    message = 'Welcome to Flexget Telegram Bot!\n'
    token = config.get('token')
    username = config.get('username')
    password = config.get('password')
    base_url = config.get('base_url')
    if token:
        valid = FlexgetRequest.verify_connection(token, base_url)
    else:
        token = FlexgetRequest.get_token(base_url, username, password)
        valid = token is not None
    if not valid:
        message += 'Could not verify credentials. Please check config file'
    bot.sendMessage(update.message.chat_id, text=message)


start_handler = CommandHandler('start', start)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text=HELP_MESSAGE)


help_handler = CommandHandler('help', help)


def register_handlers(handlers, error_handler=None, help_message=None):
    for handler in handlers:
        HANDLERS.append(handler)
    if error_handler:
        ERROR_HANDLERS.append(error_handler)
    if help_message:
        global HELP_MESSAGE
        HELP_MESSAGE += help_message


# TODO dynamically register handlers via hooks
HANDLERS.append(help_handler)
HANDLERS.append(start_handler)
register_handlers([main_conversation], help_message='/movieList - Manage movie list')
