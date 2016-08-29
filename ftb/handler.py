import logging
import os

from path import Path
from telegram.ext.commandhandler import CommandHandler

from ftb import handlers as handlers_pkg
from ftb.event import fire_event, remove_event_handlers

log = logging.getLogger(__name__)

HANDLERS = []
ERROR_HANDLERS = []
HELP_MESSAGE = ''


def _strip_trailing_sep(path):
    return path.rstrip("\\/")


def _load_handlers_from_dirs(dirs):
    """
    :param list dirs: Directories from where plugins are loaded from
    """

    log.debug('Trying to load handlers from: %s' % dirs)
    dirs = [Path(d) for d in dirs if os.path.isdir(d)]
    # add all dirs to plugins_pkg load path so that imports work properly from any of the plugin dirs
    handlers_pkg.__path__ = list(map(_strip_trailing_sep, dirs))
    for handler_dir in dirs:
        for handler_path in handler_dir.walkfiles('*.py'):
            if handler_path.name == '__init__.py':
                continue
            # Split the relative path from the plugins dir to current file's parent dir to find subpackage names
            handler_subpackages = [_f for _f in handler_path.relpath(handler_dir).parent.splitall() if _f]
            module_name = '.'.join([handlers_pkg.__name__] + handler_subpackages + [handler_path.namebase])
            try:
                __import__(module_name)
            except Exception as e:
                log.error('Cannot load handler: %s', e)
                continue


def load_handlers(extra_dirs=None):
    """
    Load plugins from the standard plugin paths.
    :param list extra_dirs: Extra directories from where plugins are loaded.
    """
    if not extra_dirs:
        extra_dirs = []

    # Import all the plugins
    _load_handlers_from_dirs(extra_dirs)
    # Register them
    fire_event('handler.register')
    # Plugins should only be registered once, remove their handlers after
    remove_event_handlers('handler.register')


def register_handlers(handler, help_message=None, error=False):
    if error:
        destination = ERROR_HANDLERS
    else:
        destination = HANDLERS
    destination.append(handler)
    if help_message:
        global HELP_MESSAGE
        HELP_MESSAGE += help_message


def get_handler_lists():
    return HANDLERS, ERROR_HANDLERS


def error(bot, update, error):
    log.warn('Update "%s" caused error "%s"' % (update, error))


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text=HELP_MESSAGE)


help_handler = CommandHandler('help', help)

# Register help handler
register_handlers(help_handler)
# Register error handler
register_handlers(error, error=True)
