import os

from telegram.ext.updater import Updater

from ftb.config import load_config
from ftb.handler import load_handlers, get_handler_lists


class FlexgetBot(object):
    def __init__(self, args, base_path, config_file='config.yml'):
        self.bot_token = args.token
        self.config_file = config_file
        load_config(os.getcwd(), self.config_file)
        load_handlers(extra_dirs=[os.path.join(base_path, 'handlers')])
        self.init_bot()

    def init_bot(self):
        updater = Updater(token=self.bot_token)
        dispatcher = updater.dispatcher

        handlers, error_handlers = get_handler_lists()
        for handler in handlers:
            dispatcher.add_handler(handler)
        for error_handler in error_handlers:
            dispatcher.add_error_handler(error_handler)
        updater.start_polling()
        updater.idle()
