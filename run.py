import os
import logging

from argparse import ArgumentParser

from ftb.bot import FlexgetBot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

parser = ArgumentParser(description='Initiate flexget telegram bot')
parser.add_argument('-t', '--token', required=True, help='Telegram bot token')

if __name__ == '__main__':
    args = parser.parse_args()
    bot = FlexgetBot(args, os.path.join(os.getcwd(), 'ftb'))
