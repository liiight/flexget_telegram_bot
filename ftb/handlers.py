import logging
import os

from path import Path
from telegram.ext.commandhandler import CommandHandler

from ftb import endpoints as endpoint_pkg
from ftb.event import fire_event, remove_event_handlers

log = logging.getLogger(__name__)

HANDLERS = []
ERROR_HANDLERS = []
HELP_MESSAGE = ''


def error(bot, update, error):
    log.warn('Update "%s" caused error "%s"' % (update, error))


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text=HELP_MESSAGE)


help_handler = CommandHandler('help', help)


def _strip_trailing_sep(path):
    return path.rstrip("\\/")


def _load_endpoints_from_dirs(dirs):
    """
    :param list dirs: Directories from where plugins are loaded from
    """

    log.debug('Trying to load endpoints from: %s' % dirs)
    dirs = [Path(d) for d in dirs if os.path.isdir(d)]
    # add all dirs to plugins_pkg load path so that imports work properly from any of the plugin dirs
    endpoint_pkg.__path__ = list(map(_strip_trailing_sep, dirs))
    for endpoint_dir in dirs:
        for endpoint_path in endpoint_dir.walkfiles('*.py'):
            if endpoint_path.name == '__init__.py':
                continue
            # Split the relative path from the plugins dir to current file's parent dir to find subpackage names
            endpoint_subpackages = [_f for _f in endpoint_path.relpath(endpoint_dir).parent.splitall() if _f]
            module_name = '.'.join([endpoint_pkg.__name__] + endpoint_subpackages + [endpoint_path.namebase])
            try:
                __import__(module_name)
            except Exception as e:
                log.error('Cannot load endpoint')
                continue


def load_endpoints(extra_dirs=None):
    """
    Load plugins from the standard plugin paths.
    :param list extra_dirs: Extra directories from where plugins are loaded.
    """
    if not extra_dirs:
        extra_dirs = []

    # Import all the plugins
    _load_endpoints_from_dirs(extra_dirs)
    # Register them
    fire_event('endpoint.register')
    # Plugins should only be registered once, remove their handlers after
    remove_event_handlers('endpoint.register')


def register_handlers(handlers, help_message=None, error=False):
    if error:
        destination = ERROR_HANDLERS
    else:
        destination = HANDLERS
    for handler in handlers:
        destination.append(handler)
    if help_message:
        global HELP_MESSAGE
        HELP_MESSAGE += help_message


def get_handler_lists():
    return HANDLERS, ERROR_HANDLERS


# Register help handler
register_handlers([help_handler])
# Register error handler
register_handlers([error], error=True)
