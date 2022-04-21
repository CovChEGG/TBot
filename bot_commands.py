from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
import datetime as dt
from greetings import greeting_phrases as greetings


def start_cmd(update: Update, context: CallbackContext):
    txt = (greetings(update.effective_user.first_name) +
            '\nИспользуйте комманду /menu если хотите узнать что бот может на текущий момент')
    update.message.reply_text(txt)


def time_cmd(update: Update, context: CallbackContext):
    dt_now = str(dt.datetime.now())
    update.message.reply_text(f'Сегодня: {dt_now[:10]}, сейчас: {dt_now[11:-7]}')


def menu_cmd(update: Update, context: CallbackContext):
    update.message.reply_text(f'/start - увидеть приветствие бота\n'
                              f'/time - узнать текущую дату и время\n'
                              f'/candies - сыграть в конфетки (забери последнюю)\n'
                              f'/menu - отобразить данное меню с описанием комманд')


# def sum_cmd(update: Update, context: CallbackContext):


def text(update: Update, context: CallbackContext):
    text_received = update.message.text
    # update.message.reply_text(f'did you said "{text_received}" ?')


# def error(update, context):
#     update.message.reply_text('an error occured')
