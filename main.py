from telegram import Bot, Update, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from telegram.error import NetworkError, Unauthorized
from bot_commands import *
from g_candies import *
from decouple import config  # хранение паролей и токенов в файле .env

start = False

updater = Updater(config('cchbot_token', default=''))
bot = Bot(config('cchbot_token', default=''))
dispatcher = updater.dispatcher

if not start:
    chat_ids = list(config('chat_id_test1', default=''))
    for all in chat_ids:
        bot.send_message(all, 'I`am online')
    start = True
dispatcher.add_handler(CommandHandler('start', start_cmd))
dispatcher.add_handler(CommandHandler('time', time_cmd))
dispatcher.add_handler(CommandHandler('candies', candies_cmd))
dispatcher.add_handler(CommandHandler('menu', menu_cmd))

dispatcher.add_handler(MessageHandler(Filters.text, text))
dispatcher.add_handler(CallbackQueryHandler(button))

# dispatcher.add_error_handler(error)

print('...on-line...')

updater.start_polling()
updater.idle()


# def stop(func: Callable) -> Callable:
#     """
#     Wrapper for func to stop current action with command "/stop"
#     """
#     def wrapped_func(*args, **kwargs):
#         message = args[0]
#         if message.text == '/stop':
#             bot.send_message(message.from_user.id, 'Текущее действие остановлено.')
#         else:
#             return func(*args, **kwargs)
#
#     return wrapped_func
#
# @cancel_proc
# @bot.message_handler(commands=['command'])
# def get_name_city(message: Optional[telebot.types.Message]) -> None:
#
#     while True:
#         bot.send_message(message.from_user.id, 'Происходит какое-то действие')