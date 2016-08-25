import io
import os

import yaml
from telegram.ext.updater import Updater


class MissingData(Exception): pass


config = {}


class FlexgetBot(object):
    def __init__(self, args, config_file='config.yml'):
        self.bot_token = args.token
        self.config_file = config_file
        global config
        config = self.load_config()
        self.init_bot()

    def load_config(self):
        config_file = os.path.join(os.getcwd(), self.config_file)
        with io.open(config_file) as file:
            config = yaml.load(file)
        self.validate_config(config)
        return config

    @staticmethod
    def validate_config(config):
        if not config.get('base_url'):
            raise MissingData('Missing base_url value in config file')
        if not (config.get('username') and config.get('password')) and not config.get('token'):
            raise MissingData('Missing credentials in config file')

    def init_bot(self):
        from ftb.handlers import HANDLERS, error
        updater = Updater(token=self.bot_token)
        dispatcher = updater.dispatcher

        for handler in HANDLERS:
            dispatcher.add_handler(handler)
        dispatcher.add_error_handler(error)
        updater.start_polling()
        updater.idle()
