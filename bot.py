# - *- coding: utf- 8 - *-
from time import time
from typing import Text
import telebot
from telebot import types

import flask
from flask import Flask
from flask import request
from flask_sslify import SSLify

import re

from datetime import datetime
from datetime import timedelta

import config

from user_class import User

import logging

from database_model import SQLighter

#logging
# logging.basicConfig(level=logging.INFO)

#Bot Config
# bot = telebot.TeleBot(config.API_TOKEN)
# bot.remove_webhook()
# bot.set_webhook(url=config.WEBHOOK_URL)

#Flask Config
# app = Flask(__name__)
# sslify = SSLify(app)
# @app.route('/' + config.secret,methods=['POST'])
# def webhook():
#      update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
#      bot.process_new_updates([update])
#      return "ok",200

#Import questions and answers

#Open questions and answers
#def first_question(message):
#chat_id = message.chat.id
#text = message.text
# all_question = questions.get_all()
# iterator = 0
# while(iterator < len(all_question)):
#     questions = all_question[iterator]
#     iterator = iterator + 1
#     markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=1)
#     
#     markup.add("Есептеу жұмыстарын орындау","Түрлі жабдықтардың нобайын жасау, жаңа техникалар ойлап шығару","Жарақаттанған адамдарға көмек көрсету","Заттардың бетіне, кітаптарға, қабырғаға салынған суреттерді тамашалау","Түрлі қатерден адамдарды қорғау және құтқару")
#       
# 
# 
# 
# 



#User class

logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(config.API_TOKEN)
bot.remove_webhook()

bot.enable_save_next_step_handlers(delay=2)
# bot.load_next_step_handlers()

data_base = SQLighter()
users = {}

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True,row_width=2)
    emoji = u"\U0001F4DA"
    text = "Тестті бастау"
    command = emoji + text

    emoji1 = u"\U0001F510"
    text1 = "Регистрация"
    command1 = emoji1 + text1
    markup.add(command1,command)

    chat_id = message.chat.id
    bot.send_message(chat_id, "Сәлеметсізбе! {0.first_name}!\nМен - <b>{1.first_name}</b>, мамандығыңызды таңдауға көмектесетін ботпын.Мамандығыңызды таңдау үшін тест тапсыру қажет.\nТест тапсыру үшін бірінші жүйеге тіркеліңіз.<b>Регистрация</b> түймесін басыңыз\nЕгер сіз регистрациядан өтіп қойған жағдайда, <b>Тестті бастау</b> түймесін басыңыз"
    .format(message.from_user, bot.get_me()),reply_markup=markup,
    parse_mode='html'
    )

emoji1 = u"\U0001F510"
text1 = "Регистрация"
command1 = emoji1 + text1
#/registration
@bot.message_handler(commands=['registration'])
@bot.message_handler(func=lambda message: message.text == command1)
def register(message):
    user_chat_id = message.chat.id
    check = data_base.user_exists(user_chat_id)

    if check == False:
        data_base.add_user_id(user_chat_id)
        msg = bot.send_message(user_chat_id, "Атыңызды теріңіз:")
        bot.register_next_step_handler(msg, register_name)
    else:
        msg = bot.send_message(user_chat_id, "Сіз регистрациядан өтіп қойғансыз, /test_start командасын басыңыз")

#register name
def register_name(message):
    text = message.text
    user_chat_id = message.chat.id
    if text is not None:
        data_base.add_user_name(user_chat_id,text)
        msg = bot.send_message(user_chat_id,"Атыңыз базаға енгізілді, енді фамилияңызды теріңіз")
        bot.register_next_step_handler(msg, register_last_name)
    else:
        msg = bot.send_message(user_chat_id, "Атыңызды қайтадан теріңіз")
        bot.register_next_step_handler(msg,register_name)

#register last name
def register_last_name(message):
    text = message.text
    user_chat_id = message.chat.id
    if text is not None:
        data_base.add_user_last_name(user_chat_id,text)
        msg = bot.send_message(user_chat_id,"Фамилияңыз базаға енгізілді, енді телефон номеріңізді теріңіз")
        bot.register_next_step_handler(msg, register_phone_number)
    else:
        msg = bot.send_message(user_chat_id, "Фамилияңызды қайтадан теріңіз")
        bot.register_next_step_handler(msg,register_last_name)

#register phone number
def register_phone_number(message):
    text = message.text
    user_chat_id = message.chat.id

    if re.match(r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$",text):
        data_base.add_user_phone_number(user_chat_id,text)
        msg = bot.send_message(user_chat_id,"Телефон номеріңіз базаға тіркелді.\nРегистрация аяқталды.Тест тапсыру үшін /test_start командасын басыңыз")
    else:
        msg = bot.send_message(user_chat_id, "Номеріңізді қайтадан теріңіз")
        bot.register_next_step_handler(msg,register_phone_number)


#test section
emoji = u"\U0001F4DA"
text = "Тестті бастау"
command = emoji + text
@bot.message_handler(func=lambda message: message.text == command)
@bot.message_handler(commands=['test_start'])
def test_start(message):
    user_chat_id = message.chat.id
    check = data_base.user_exists(user_chat_id)

    if check == True:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=1)
        markup.add('Шығынды есептеу', 'Машиналарды, құралдарды құрастыру', 'Табиғи құбылыстарға,өсімдіктердің өсуіне,т.б.бақылау жасау',"Бақылаған немесе ойыңдағы оқиғаларды көркем тілмен суреттеу","Қиындыққа тап болғандарға көмек көрсететін органдарға жол сілтеу")

        user = data_base.user_get_all(user_chat_id)

        default_time_str = "01/01/1970 00:00:00"

        default_date = datetime.strptime(default_time_str, '%d/%m/%Y %H:%M:%S')

        test_time = datetime.strptime(user[5], '%d/%m/%Y %H:%M:%S')

        date_now = datetime.now() + timedelta(hours=6)

        date_test_can = test_time + timedelta(days=1)

        if test_time == default_date:
            user = User()
            users[user_chat_id] = user
            user.chat_id = user_chat_id
            bot.send_message(user_chat_id, "Тестті бастаймыз!")
            msg = bot.send_message(user_chat_id, "Сізге не ұнайды? Пернетақта арқылы жауап беріңіз",reply_markup=markup)
            bot.register_next_step_handler(msg, first_question1)
        elif test_time > default_date and date_test_can > date_now:

            date_test_can_str = datetime.strftime(date_test_can, '%d/%m/%Y %H:%M:%S')

            bot.send_message(user_chat_id, f"Кешіріңіз, сiз тестті уақытша тапсыра алмайсыз.Сіз осы уақыттан бастап {date_test_can_str} тапсыра аласыз")
        else:
            # user = User()
            # users[user_chat_id] = user
            # user.chat_id = user_chat_id
            bot.send_message(user_chat_id, "Cіз тестті қайтадан тапсыра аласыз!")
            msg = bot.send_message(user_chat_id, "Сізге не ұнайды? Пернетақта арқылы жауап беріңіз",reply_markup=markup)
            bot.register_next_step_handler(msg, first_question1)

    else:
        bot.send_message(user_chat_id, "Тестті тапсыру үшін бірінші регистрациядан өту керек. /registration командасын басыңыз")

# def ask_questions(message):
#     all_question = questions.get_all()
#     iterator = 0
#     while(iterator < len(all_question)):
#         chat_id = message.chat.id
#         text = message.text

#         questions_dict = all_question[iterator]
#         list_questions = list(questions_dict.keys())
#         list_answers = list(questions_dict.values())

#         if text == list_questions[0]:
#             data_base.add_user_test_result(chat_id,list_answers[0])
#         elif text == list_questions[1]:
#             data_base.add_user_test_result(chat_id,list_questions[1])
#         elif text == list_questions[2]:
#             data_base.add_user_test_result(chat_id,list_questions[2])
#         elif text == list_questions[3]:
#             data_base.add_user_test_result(chat_id,list_questions[3])
#         elif text == list_questions[4]:
#             data_base.add_user_test_result(chat_id,list_questions[4])

#         iterator = iterator + 1

#         next_questions = all_question[iterator]
#         markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=1)
#         markup.add(next_questions[0],next_questions[1],next_questions[2],next_questions[3],next_questions[4])

#         msg = bot.send_message(chat_id, "Сізге не ұнайды?",reply_markup=markup)

def first_question1(message):
    chat_id=message.chat.id
    text = message.text

    user = users[chat_id]

    #Ответы вариантов для 2 вопроса
    markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=1)
    markup1.add("Есептеу жұмыстарын орындау","Түрлі жабдықтардың нобайын жасау, жаңа техникалар ойлап шығару","Жарақаттанған адамдарға көмек көрсету","Заттардың бетіне, кітаптарға, қабырғаға салынған суреттерді тамашалау","Түрлі қатерден адамдарды қорғау және құтқару")

    if text == "Шығынды есептеу":
        user.totalsum = user.totalsum + 1
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup1)
        bot.register_next_step_handler(msg, second_question)
    elif text == "Машиналарды, құралдарды құрастыру":
        user.totalsum = user.totalsum + 2
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup1)
        bot.register_next_step_handler(msg, second_question)
    elif text == "Табиғи құбылыстарға,өсімдіктердің өсуіне,т.б.бақылау жасау":
        user.totalsum = user.totalsum + 3
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup1)
        bot.register_next_step_handler(msg, second_question)
    elif text == "Бақылаған немесе ойыңдағы оқиғаларды көркем тілмен суреттеу":
        user.totalsum = user.totalsum + 4
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup1)
        bot.register_next_step_handler(msg, second_question)
    elif text == "Қиындыққа тап болғандарға көмек көрсететін органдарға жол сілтеу":
        user.totalsum = user.totalsum + 5
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup1)
        bot.register_next_step_handler(msg, second_question)
    else:
         msg = bot.send_message(chat_id, "Жауабыңыз дұрыс емес,берілген варианттар арқылы жауап беріңіз",)
         bot.register_next_step_handler(msg, first_question1)
         return

def second_question(message):
    chat_id=message.chat.id
    text = message.text

    user = users[chat_id]

    #Варианты ответов для 3 вопроса
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=1)
    markup.add("Ғылыми кітаптарды оқып, талқылау","Ғимараттардың, техникалық машиналардың жобасын сызу","Микроб, бактериялардың тіршілігін бақылау","Көркемөнер үйірмелерінің жұмыстарын бақылау","Кедергілерді жан-жақты қарастырып, қиындықты шешудің оңай жолын іздестіру")

    if text == "Есептеу жұмыстарын орындау":
        user.totalsum = user.totalsum + 1
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, third_question)
    elif text == "Түрлі жабдықтардың нобайын жасау, жаңа техникалар ойлап шығару":
        user.totalsum = user.totalsum + 2
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, third_question)
    elif text == "Жарақаттанған адамдарға көмек көрсету":
        user.totalsum = user.totalsum + 3
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, third_question)
    elif text == "Заттардың бетіне, кітаптарға, қабырғаға салынған суреттерді тамашалау":
        user.totalsum = user.totalsum + 4
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, third_question)
    elif text == "Түрлі қатерден адамдарды қорғау және құтқару":
        user.totalsum = user.totalsum + 5
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, third_question)
    else:
         msg = bot.send_message(chat_id, "Жауабыңыз дұрыс емес,берілген варианттар арқылы жауап беріңіз",)
         bot.register_next_step_handler(msg, second_question)
         return

def third_question(message):
    chat_id=message.chat.id
    text = message.text

    user = users[chat_id]

    #Варианты ответов для 4 вопроса
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=1)
    markup.add("Тауардың артықшылығын анықтап,тұтынушыға түсіндіру,сату","Өнеркәсіп бұйымдарының жаңа түрлерін шығару,жобасын жасау","Өсімдіктердің жаңа сорттарын ойлап шығару","Көркем әдебиетті оқу, талқылау","Заңды және заңсыз оқиғалар")

    if text == "Ғылыми кітаптарды оқып, талқылау":
        user.totalsum = user.totalsum + 1
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, fourth_question)
    elif text == "Ғимараттардың, техникалық машиналардың жобасын сызу":
        user.totalsum = user.totalsum + 2
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, fourth_question)
    elif text == "Микроб, бактериялардың тіршілігін бақылау":
        user.totalsum = user.totalsum + 3
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, fourth_question)
    elif text == "Көркемөнер үйірмелерінің жұмыстарын бақылау":
        user.totalsum = user.totalsum + 4
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, fourth_question)
    elif text == "Кедергілерді жан-жақты қарастырып, қиындықты шешудің оңай жолын іздестіру":
        user.totalsum = user.totalsum + 5
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, fourth_question)
    else:
         msg = bot.send_message(chat_id, "Жауабыңыз дұрыс емес,берілген варианттар арқылы жауап беріңіз",)
         bot.register_next_step_handler(msg, third_question)
         return

def fourth_question(message):
    chat_id=message.chat.id
    text = message.text

    user = users[chat_id]

    #Варианты для пятого вопроса
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=1)
    markup.add("Статистикалық мәліметтер жасау,жинақтау","Ағаштан,темірден,пластмассадан,қағаздан түрлі бұйым жасау","Науқастарды қабылдап,сөйлесіп,ем тағайындау","Әдемі құбылыстарды суретке түсіру","Кестелерден,кітаптардан,суреттерден қатесін іздеп табу")

    if text == "Тауардың артықшылығын анықтап,тұтынушыға түсіндіру,сату":
        user.totalsum = user.totalsum + 1
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, fifth_question)
    elif text == "Өнеркәсіп бұйымдарының жаңа түрлерін шығару,жобасын жасау":
        user.totalsum = user.totalsum + 2
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, fifth_question)
    elif text == "Өсімдіктердің жаңа сорттарын ойлап шығару":
        user.totalsum = user.totalsum + 3
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, fifth_question)
    elif text == "Көркем әдебиетті оқу, талқылау":
        user.totalsum = user.totalsum + 4
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, fifth_question)
    elif text == "Заңды және заңсыз оқиғалар":
        user.totalsum = user.totalsum + 5
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, fifth_question)
    else:
         msg = bot.send_message(chat_id, "Жауабыңыз дұрыс емес,берілген варианттар арқылы жауап беріңіз",)
         bot.register_next_step_handler(msg, fourth_question)
         return

def fifth_question(message):
    chat_id=message.chat.id
    text = message.text

    user = users[chat_id]

    #Варианты ответов для 6 вопроса
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=1)
    markup.add("Кез-келген өнімнің пайдасы мен зиянын саралау","Құрылыстың сызбасын сызу","Кез-келген заттың құрамын анықтау","Сахнада өнер көрсету,концертке қатысу,музыкалық аспапта ойнау","Адамдар арасындағы дауды шешу, түсіндіру")

    if text == "Статистикалық мәліметтер жасау,жинақтау":
        user.totalsum = user.totalsum + 1
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, sixth_question)
    elif text == "Ағаштан,темірден,пластмассадан,қағаздан түрлі бұйым жасау":
        user.totalsum = user.totalsum + 2
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, sixth_question)
    elif text == "Науқастарды қабылдап,сөйлесіп,ем тағайындау":
        user.totalsum = user.totalsum + 3
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, sixth_question)
    elif text == "Әдемі құбылыстарды суретке түсіру":
        user.totalsum = user.totalsum + 4
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, sixth_question)
    elif text == "Кестелерден,кітаптардан,суреттерден қатесін іздеп табу":
        user.totalsum = user.totalsum + 5
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, sixth_question)
    else:
         msg = bot.send_message(chat_id, "Жауабыңыз дұрыс емес,берілген варианттар арқылы жауап беріңіз",)
         bot.register_next_step_handler(msg, fifth_question)
         return

def sixth_question(message):
    chat_id=message.chat.id
    text = message.text

    user = users[chat_id]

    #Варианты ответов для 7 вопроса
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=1)
    markup.add("Сатып алушы мен сатушының пайдасын есептеу","Есептеу машинасына бағдарлама жасау","Құстың балапанын немесе мал өсірген","Басқаларды аузыма қаратып,жақсы көңіл күй сыйлау","Кішкентай балаларға тапсырма беріп,қалай орындағанын бақылау")

    if text == "Кез-келген өнімнің пайдасы мен зиянын саралау":
        user.totalsum = user.totalsum + 1
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, seventh_question)
    elif text == "Құрылыстың сызбасын сызу":
        user.totalsum = user.totalsum + 2
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, seventh_question)
    elif text == "Кез-келген заттың құрамын анықтау":
        user.totalsum = user.totalsum + 3
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, seventh_question)
    elif text == "Сахнада өнер көрсету,концертке қатысу,музыкалық аспапта ойнау":
        user.totalsum = user.totalsum + 4
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, seventh_question)
    elif text == "Адамдар арасындағы дауды шешу, түсіндіру":
        user.totalsum = user.totalsum + 5
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, seventh_question)
    else:
         msg = bot.send_message(chat_id, "Жауабыңыз дұрыс емес,берілген варианттар арқылы жауап беріңіз",)
         bot.register_next_step_handler(msg, sixth_question)
         return

def seventh_question(message):
    chat_id=message.chat.id
    text = message.text

    user = users[chat_id]

    #Варианты ответов для 8 вопроса
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=1)
    markup.add("Өсуді немесе кемуді көрсететін кестелер,диаграммалар жасау","Пернелі машиналармен жұмыс істеу","Жан-жануарларды емдеу, күтім жасау","Көрмелер,сахналарды көркемдік жағынан безендіру","Қатарластарыңды,кіші жастағыларды туристік саяхатқа,мұражайларға апарған")

    if text == "Сатып алушы мен сатушының пайдасын есептеу":
        user.totalsum = user.totalsum + 1
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, eighth_question)
    elif text == "Есептеу машинасына бағдарлама жасау":
        user.totalsum = user.totalsum + 2
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, eighth_question)
    elif text == "Құстың балапанын немесе мал өсірген":
        user.totalsum = user.totalsum + 3
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, eighth_question)
    elif text == "Басқаларды аузыма қаратып,жақсы көңіл күй сыйлау":
        user.totalsum = user.totalsum + 4
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, eighth_question)
    elif text == "Кішкентай балаларға тапсырма беріп,қалай орындағанын бақылау":
        user.totalsum = user.totalsum + 5
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, eighth_question)
    else:
         msg = bot.send_message(chat_id, "Жауабыңыз дұрыс емес,берілген варианттар арқылы жауап беріңіз",)
         bot.register_next_step_handler(msg, seventh_question)
         return

def eighth_question(message):
    chat_id=message.chat.id
    text = message.text

    user = users[chat_id]

    #Варианты ответов для 9 вопроса
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,row_width=1)
    markup.add("Кесте жасау, кез-келген іске қанша уақыт жұмсалатынын есептеу","Сызбаларды, кестелерді түсіну, тексеру, анықтау, түзету","Өсімдіктердің, орман ағаштарының сырқатын емдеу","Киімдерді, заттардың пішінін өзгертіп, жөндеу","Адамдарға қажетті мәліметтерді түсіндіру")

    if text == "Өсуді немесе кемуді көрсететін кестелер,диаграммалар жасау":
        user.totalsum = user.totalsum + 1
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, nineth_question)
    elif text == "Пернелі машиналармен жұмыс істеу":
        user.totalsum = user.totalsum + 2
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, nineth_question)
    elif text == "Жан-жануарларды емдеу, күтім жасау":
        user.totalsum = user.totalsum + 3
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, nineth_question)
    elif text == "Көрмелер,сахналарды көркемдік жағынан безендіру":
        user.totalsum = user.totalsum + 4
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, nineth_question)
    elif text == "Қатарластарыңды,кіші жастағыларды туристік саяхатқа,мұражайларға апарған":
        user.totalsum = user.totalsum + 5
        msg = bot.send_message(chat_id,"Сізге не ұнайды?\nМаған тек берілген варианттар арқылы жауап бересіз",reply_markup=markup)
        bot.register_next_step_handler(msg, nineth_question)
    else:
         msg = bot.send_message(chat_id, "Жауабыңыз дұрыс емес,берілген варианттар арқылы жауап беріңіз",)
         bot.register_next_step_handler(msg, eighth_question)
         return

def nineth_question(message):
    chat_id=message.chat.id
    text = message.text

    user = users[chat_id]

    if text == "Кесте жасау, кез-келген іске қанша уақыт жұмсалатынын есептеу":
        user.totalsum = user.totalsum + 1
        test_object = datetime.now() + timedelta(hours=6)
        date_test_can_str = datetime.strftime(test_object, '%d/%m/%Y %H:%M:%S')
        data_base.add_user_test_time(chat_id,date_test_can_str)
        bot.send_message(chat_id,"Тест аяқталды.Жауабын білу үшін /test_result командасын басыңыз")
    elif text == "Сызбаларды, кестелерді түсіну, тексеру, анықтау, түзету":
        user.totalsum = user.totalsum + 2
        test_object = datetime.now() + timedelta(hours=6)
        date_test_can_str = datetime.strftime(test_object, '%d/%m/%Y %H:%M:%S')
        data_base.add_user_test_time(chat_id,date_test_can_str)
        bot.send_message(chat_id,"Тест аяқталды.Жауабын білу үшін /test_result командасын басыңыз")
    elif text == "Өсімдіктердің, орман ағаштарының сырқатын емдеу":
        user.totalsum = user.totalsum + 3
        test_object = datetime.now() + timedelta(hours=6)
        date_test_can_str = datetime.strftime(test_object, '%d/%m/%Y %H:%M:%S')
        data_base.add_user_test_time(chat_id,date_test_can_str)
        bot.send_message(chat_id,"Тест аяқталды.Жауабын білу үшін /test_result командасын басыңыз")
    elif text == "Киімдерді, заттардың пішінін өзгертіп, жөндеу":
        user.totalsum = user.totalsum + 4
        test_object = datetime.now() + timedelta(hours=6)
        date_test_can_str = datetime.strftime(test_object, '%d/%m/%Y %H:%M:%S')
        data_base.add_user_test_time(chat_id,date_test_can_str)
        bot.send_message(chat_id,"Тест аяқталды.Жауабын білу үшін /test_result командасын басыңыз")
    elif text == "Адамдарға қажетті мәліметтерді түсіндіру":
        user.totalsum = user.totalsum + 5
        test_object = datetime.now() + timedelta(hours=6)
        date_test_can_str = datetime.strftime(test_object, '%d/%m/%Y %H:%M:%S')
        data_base.add_user_test_time(chat_id,date_test_can_str)
        bot.send_message(chat_id,"Тест аяқталды.Жауабын білу үшін /test_result командасын басыңыз")
    else:
         msg = bot.send_message(chat_id, "Жауабыңыз дұрыс емес,берілген варианттар арқылы жауап беріңіз",)
         bot.register_next_step_handler(msg, nineth_question)
         return

#test result
@bot.message_handler(commands=['test_result'])
def test_result(message):
    chat_id = message.chat.id
    check = data_base.user_exists(chat_id)

    if check == True:
        exists = chat_id in users
        if exists == True:
            user = users[chat_id] 
            user_result = user.totalsum
            data_base.add_user_test_result(chat_id,user_result)
            get_data = data_base.user_get_all(chat_id)
            your_result = get_data[6]
            bot.send_message(chat_id,f"Cіздің көрсеткішіңіз:{int(your_result)}")
        else:
            get_data = data_base.user_get_all(chat_id)
            your_result = get_data[6]
            bot.send_message(chat_id,f"Cіздің көрсеткішіңіз:{int(your_result)}")
    if check == False:
        bot.send_message(chat_id, "Сіз әлі тесттен өткен жоқсыз.",)


#FAQ command
bot.polling(none_stop=True)