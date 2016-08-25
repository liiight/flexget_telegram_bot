from argparse import ArgumentParser

from telegram.error import Unauthorized, InvalidToken
from telegram.ext.updater import Updater

from ftb.handlers import HANDLERS, error

parser = ArgumentParser(description='Initiate flexget telegram bot')
parser.add_argument('-t', '--token', required=True, help='Telegram bot token')


def init_bot(token):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    for handler in HANDLERS:
        dispatcher.add_handler(handler)
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    args = parser.parse_args()
    try:
        init_bot(args.token)
    except (InvalidToken, Unauthorized) as e:
        print('ERROR: %s' % e)
        exit()
