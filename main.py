
#Имя: Школьный бот Боб


import telebot
from telebot import types
from services import *


from config import keys
from config import TOKEN


bot = telebot.TeleBot(TOKEN)



button_one = types.KeyboardButton(text='Уроки Алина')
button_two = types.KeyboardButton(text='Уроки Лера')


@bot.message_handler(commands=['start'])
def process_start_command(message: telebot.types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(button_one, button_two)

    bot.send_message(message.chat.id, 'Посмотрим', reply_markup=keyboard)


@bot.message_handler(content_types=['text', ])
def repeat(message: telebot.types.Message):

    try:
        value = message.text.split(' ')

        if len(value) >= 3:
            raise APIException('Много введено параметров.')

        if len(value) == 2:
            command, name = value
            if (command == 'уроки') or (command == 'Уроки'):
                result = GetLesson.get_lessons(keys[name], command)
                if result:
                    s = ''
                    for i in result:
                        s = s + i + ';\n\n'

                    bot.send_message(message.chat.id, s)


    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду:\n{e}")



if __name__ == '__main__':
    # bot.stop_polling();
    bot.polling(none_stop=True, interval=1)




