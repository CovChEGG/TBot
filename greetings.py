from random import randint


def greeting_phrases(name, style=0):
    official_l = [f'Приветствую Вас, {name}!', f'Здравствуйте, {name}!',
                  f'{name}, рад Вас снова приветствовать!']
    friendly_l = [f'Привет, {name}', f'{name}, привет!',
                  f'{name}, cалют!', f'Хай, {name}', f'Как сам, {name}?']
    if style == 1:
        phrases = official_l
    elif style == 2:
        phrases = friendly_l
    else:
        phrases = official_l + friendly_l
    return phrases[randint(0, len(phrases) - 1)]
