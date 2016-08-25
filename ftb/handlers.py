import logging

from telegram.ext.commandhandler import CommandHandler

from ftb.endpoints.movie_list import main_conversation

logger = logging.getLogger(__name__)

HANDLERS = []
ERROR_HANDLERS = []
HELP_MESSAGE = ''


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
register_handlers([main_conversation, help_handler], help_message='/movieList - Manage movie list')
