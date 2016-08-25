from argparse import ArgumentParser

from telegram.error import Unauthorized, InvalidToken

from ftb.bot import FlexgetBot, MissingData

parser = ArgumentParser(description='Initiate flexget telegram bot')
parser.add_argument('-t', '--token', required=True, help='Telegram bot token')

if __name__ == '__main__':
    args = parser.parse_args()
    bot = FlexgetBot(args)
