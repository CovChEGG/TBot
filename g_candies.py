from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import time
from emoji import emojize
from random import randint
from bot_commands import menu_cmd


ON = 1
OFF = 0
candies_mode = OFF

NO_DEF = 0
VS_BOT = 1
VS_USR = 2
game_mode = NO_DEF

NO_MOV = 0
FIRST_M = 1
SECOND_M = 2
move_turn = NO_MOV

number_of_candies = 10
min_take = 1
max_take = 3


def default_candies(cand_mode=OFF, candies_def=0, min_def=1, max_def=3):
    global candies_mode, move_turn, game_mode, \
        number_of_candies, min_take, max_take
    number_of_candies = candies_def if candies_def else randint(10, 25)
    min_take = min_def
    max_take = max_def
    candies_mode = ON if cand_mode else OFF
    game_mode = NO_DEF
    move_turn = NO_MOV
    # number_of_candies = 10


def candies_cmd(update: Update, context: CallbackContext):
    global candies_mode
    default_candies(ON)
    keyboard = [
        [InlineKeyboardButton("С ботом", callback_data='1'),
         InlineKeyboardButton("С другим игроком", callback_data='2')]]
    context.bot.send_message(update.effective_chat.id, "Начинаем игру!\nВыбери режим игры",
                             reply_markup=InlineKeyboardMarkup(keyboard))


def vs_comp(update: Update, context: CallbackContext):
    global number_of_candies
    keyboard = [
        [InlineKeyboardButton("Хочу первым!", callback_data='3'),
         InlineKeyboardButton("Хожу вторым, даю фору", callback_data='4')]]
    context.bot.send_message(update.effective_chat.id,
                             f'Вы выбрали режим игры с ботом!\nВсего конфет: {number_of_candies}\nКто начинает?',
                             reply_markup=InlineKeyboardMarkup(keyboard))


def player_turn(update: Update, context: CallbackContext):
    global number_of_candies
    user_name = update.effective_user.first_name
    if number_of_candies >= 3:
        keyboard = [
            [InlineKeyboardButton("1", callback_data='5'),
             InlineKeyboardButton("2", callback_data='6'),
             InlineKeyboardButton("3", callback_data='7')]]
    if number_of_candies == 2:
        keyboard = [
            [InlineKeyboardButton(f"Беру одну, хочу проиграть", callback_data='5'),
             InlineKeyboardButton("2", callback_data='6')]]
    if number_of_candies == 1:
        keyboard = [
            [InlineKeyboardButton("Забираю последнюю! Ура!", callback_data='5')]]
    context.bot.send_message(update.effective_chat.id,
                             f'{user_name}, сколько конфет возьмёте?',
                             reply_markup=InlineKeyboardMarkup(keyboard))


def one_more(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Давай ещё!", callback_data='more_candies'),
         InlineKeyboardButton("Пожалуй хватит", callback_data='enough_candies')]]
    context.bot.send_message(update.effective_chat.id, "Попробуем ещё?",
                                reply_markup=InlineKeyboardMarkup(keyboard))


def button(update, context):
    global game_mode, move_turn, number_of_candies, min_take, max_take, VS_BOT, VS_USR, candies_mode_on
    query = update.callback_query
    query.answer()
    if candies_mode == OFF:
        if query.data == 'more_candies':
            context.bot.send_message(update.effective_chat.id,
                                     'Приступимс-с-с!')
            candies_cmd(update, context)
        elif query.data == 'enough_candies':
            context.bot.send_message(update.effective_chat.id, f'/start - увидеть приветствие бота\n'
                                      f'/time - узнать текущую дату и время\n'
                                      f'/candies - сыграть в конфетки (забери последнюю)\n'
                                      f'/menu - отобразить данное меню с описанием комманд')
        return
    if game_mode == NO_DEF:
        if query.data == "1":
            game_mode = VS_BOT
            vs_comp(update, context)
        elif query.data == "2":
            context.bot.send_message(update.effective_chat.id,
                                     'Вы выбрали режим игры с другим игроком!')
            # game_mode = VS_USR
            game_mode = VS_BOT
            vs_comp(update, context)
    if game_mode == VS_BOT:  # против компьютера
        if move_turn == NO_MOV:
            if query.data == "3":
                context.bot.send_message(update.effective_chat.id,
                                         'Вы ходите первым!')
                move_turn = FIRST_M
                player_turn(update, context)
            elif query.data == "4":
                context.bot.send_message(update.effective_chat.id,
                                         'Вы ходите вторым!')
                move_turn = SECOND_M
        elif move_turn == FIRST_M:
            if query.data == "5":
                number_of_candies -= 1
            elif query.data == "6":
                number_of_candies -= 2
            elif query.data == "7":
                number_of_candies -= 3
            if number_of_candies == 0:
                context.bot.send_message(update.effective_chat.id,
                                         'Вы победили! ' + emojize(':1st_place_medal:'))
                default_candies()
                one_more(update, context)
            else:
                move_turn = SECOND_M
                context.bot.send_message(update.effective_chat.id,
                                         f'Осталось конфет: {number_of_candies}')
        if move_turn == SECOND_M:
            # context.bot.send_message(update.effective_chat.id, 'Бот не думает, он тупо ходит...')
            # TODO прогресс-бар раздумий
            computer_take = computer_turn(min_take, max_take, number_of_candies)
            context.bot.send_message(update.effective_chat.id,
                                     'Бот взял конфет: {}.'.format(computer_take))
            number_of_candies -= computer_take
            if number_of_candies == 0:
                default_candies()
                context.bot.send_message(update.effective_chat.id,
                                         'Победил бот! ' + emojize(':laptop:') + emojize(':1st_place_medal:'))
                default_candies()
                one_more(update, context)
            else:
                move_turn = 1
                context.bot.send_message(update.effective_chat.id,
                                         f'Осталось конфет: {number_of_candies}')
                player_turn(update, context)
    # if not candies_mode_on:
    #     if query.data == "more_candies":
    #         candies_cmd()
    #     elif query.data == "enough_candies":
    #         context.bot.send_message(update.effective_chat.id,
    #                                  'Приятно было с Вами потягаться!')
    #         start_cmd

    # if game_mode == 2:


def computer_turn(min_num, max_num, num_of_cand):
    best_turn = num_of_cand % (max_num + 1)
    if best_turn == 0:
        best_turn = randint(min_num, max_num)
    return best_turn
