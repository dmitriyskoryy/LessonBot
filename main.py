
#Имя: Школьный бот Боб
#Никнейм: SchoolBotBob39


import telebot
from services import *


from config import keys
from config import TOKEN



bot = telebot.TeleBot(TOKEN)



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

        # if len(value) == 3:
        #     a, command, b = value
        #     result = Calc.get_value(a, command, b)
        #     bot.send_message(message.chat.id, result)

    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду:\n{e}")



if __name__ == '__main__':
    # bot.stop_polling();
    bot.polling(none_stop=True, interval=1)




