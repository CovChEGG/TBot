from telegram import Update, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from telegram.error import NetworkError, Unauthorized
from bot_commands import *
from g_candies import *
from decouple import config # хранение паролей и токенов в файле .env


updater = Updater(config('cchbot_token', default=''))
dispatcher = updater.dispatcher

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
