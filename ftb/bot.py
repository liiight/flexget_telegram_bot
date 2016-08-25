from telegram.ext import Updater

from ftb.endpoints.movie_list import main_conversation, help_handler, error

TELEGRAM_TOKEN = '140630506:AAFTmlwhbd-2XNWPJ7sE9Z95HRkd6XRNX-k'
HANDLERS = []

updater = Updater(token=TELEGRAM_TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(main_conversation)
dispatcher.add_handler(help_handler)
dispatcher.add_error_handler(error)

updater.start_polling()
