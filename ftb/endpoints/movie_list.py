import logging

from telegram.ext.commandhandler import CommandHandler
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext.messagehandler import MessageHandler, Filters
from telegram.ext.regexhandler import RegexHandler
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup

from ftb.api import FlexgetRequest
from ftb.event import event
from ftb.handlers import register_handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

ACTION_SELECTOR, LIST_MOVIES, ADD_MOVIES, SELECT_LIST, SHOW_MOVIES, MOVIE_NAME, MOVIE_YEAR = range(7)

MOVIE_LISTS = [{}]
MOVIE_ADD_DICT = {}

request = FlexgetRequest()


############


def get_movie_lists():
    lists = request.get('/movie_list/')
    global MOVIE_LISTS
    MOVIE_LISTS = lists['movie_lists']


def get_movies_by_list_name(list_name):
    list_id = None
    for ml in MOVIE_LISTS:
        if list_name == ml['name']:
            list_id = ml['id']
            break
    if not list_id:
        raise Exception
    movies = request.get('/movie_list/' + str(list_id) + '/movies/')
    return movies['movies']


def add_movie_to_list():
    global MOVIE_ADD_DICT
    list_id = MOVIE_ADD_DICT.pop('list_id')
    request.post('/movie_list/' + str(list_id) + '/movies/', data=MOVIE_ADD_DICT)


##################################

def main_menu(bot, update):
    keyboard = [['List', 'Add']]
    bot.sendMessage(update.message.chat_id,
                    text='Please select an action or /cancel',
                    reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return ACTION_SELECTOR


def action_selection(bot, update):
    action = update.message.text
    get_movie_lists()
    reply_keyboard = [[ml['name'] for ml in MOVIE_LISTS]]
    bot.sendMessage(update.message.chat_id,
                    text='Please select a movie list or /cancel',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    if action == 'List':
        return LIST_MOVIES
    elif action == 'Add':
        return ADD_MOVIES


def add_movies(bot, update):
    list_name = update.message.text
    get_movie_lists()
    list_id = None
    for ml in MOVIE_LISTS:
        if ml['name'] == list_name:
            list_id = ml['id']
            break
    if not list_id:
        raise Exception
    global MOVIE_ADD_DICT
    MOVIE_ADD_DICT = {'list_id': list_id}
    bot.sendMessage(update.message.chat_id,
                    text='Please send the movie title or /cancel')
    return MOVIE_NAME


def movie_name(bot, update):
    movie_name = update.message.text
    global MOVIE_ADD_DICT
    MOVIE_ADD_DICT['movie_name'] = movie_name
    bot.sendMessage(update.message.chat_id,
                    text='Please select the movie year or /skip')
    return MOVIE_YEAR


def movie_year(bot, update):
    movie_year = update.message.text
    global MOVIE_ADD_DICT
    MOVIE_ADD_DICT['movie_year'] = int(movie_year)
    add_movie_to_list()
    bot.sendMessage(update.message.chat_id, text='Movie {} successfully added'.format(MOVIE_ADD_DICT['movie_name']))
    return ConversationHandler.END


def skip_movie_year(bot, update):
    add_movie_to_list()
    bot.sendMessage(update.message.chat_id, text='Movie {} successfully added'.format(MOVIE_ADD_DICT['movie_name']))
    return ConversationHandler.END


def show_movies(bot, update):
    list_name = update.message.text
    movies = get_movies_by_list_name(list_name)
    reply = 'Movies:\n' if movies else 'No movies in list'
    for movie in movies:
        reply += '{}\n'.format(movie['title'])
    bot.sendMessage(update.message.chat_id, text=reply)

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    bot.sendMessage(update.message.chat_id,
                    text='Operation canceled')

    return ConversationHandler.END


help_handler = CommandHandler('help', help)

show_movies_cnv_handler = RegexHandler('\w', show_movies)

add_movie_cnv_handler = ConversationHandler(
    entry_points=[RegexHandler('\w', add_movies)],
    states={
        MOVIE_NAME: [MessageHandler([Filters.text], movie_name)],
        MOVIE_YEAR: [RegexHandler(r'[\d]{4}', movie_year),
                     CommandHandler('skip', skip_movie_year)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

movie_list_handler = ConversationHandler(
    entry_points=[CommandHandler('movieList', main_menu)],
    states={
        ACTION_SELECTOR: [MessageHandler([Filters.text], action_selection)],
        LIST_MOVIES: [show_movies_cnv_handler],
        ADD_MOVIES: [add_movie_cnv_handler]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)


@event('endpoint.register')
def register():
    register_handlers([movie_list_handler], help_message='/movieList - Manage movie list')
