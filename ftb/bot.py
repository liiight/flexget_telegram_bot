import os

from telegram.ext.updater import Updater

from ftb.config import load_config
from ftb.handlers import load_endpoints


class FlexgetBot(object):
    def __init__(self, args, base_path, config_file='config.yml'):
        self.bot_token = args.token
        self.config_file = config_file
        load_config(os.getcwd(), self.config_file)
        load_endpoints(extra_dirs=[os.path.join(base_path, 'endpoints')])
        self.init_bot()

    def init_bot(self):
        from ftb.handlers import HANDLERS, error
        updater = Updater(token=self.bot_token)
        dispatcher = updater.dispatcher

        for handler in HANDLERS:
            dispatcher.add_handler(handler)
        dispatcher.add_error_handler(error)
        updater.start_polling()
        updater.idle()
