import os
import logging

from telegram.ext.updater import Updater

from ftb.config import load_config
from ftb.handler import load_handlers, get_handler_lists

logging.basicConfig(filename='ftb.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

log = logging.getLogger(__name__)


class FlexgetBot(object):
    def __init__(self, args):
        log.debug('Initializing FlexgetBot')
        self.bot_token = args.token
        self.config_file = args.config
        load_config(os.getcwd(), self.config_file)
        load_handlers(extra_dirs=[os.path.join(os.getcwd(), 'ftb', 'handlers')])
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
