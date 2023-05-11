from PIL import Image
import telebot
from telebot import types
import random
import os
import json
from pyowm import OWM

bot = telebot.TeleBot('')

def get_location(lat, lon):
    url=f"https://yandex.ru/pogoda/maps/nowcast?lat={lat}&lon={lon}&via=hnav&le_Lightning=1"
    return url

def weather(city: str):
    owm=OWM("482833602a3b416d53c156c563297579")
    mgr=owm.weather_manager()
    observation=mgr.weather_at_place(city)
    weather=observation.weather
    location=get_location(observation.location.lat, observation.location.lon)
    temperature=weather.temperature("celsius")
    return temperature, location

@bot.message_handler(commands=['start'])
def start(message):
    photo = open('qu.jpg', 'rb')
    m = f' Привет, <b>{message.from_user.first_name}</b>, ты это тыкай вот на эту команду кнопки появятся /naw'
    bot.send_photo(message.chat.id, photo, m, parse_mode='html')

@bot.message_handler(commands=['naw'])
def website(message):
    ma = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    p1 = types.KeyboardButton('Фильмы')
    p2 = types.KeyboardButton('Картинки')
    p3 = types.KeyboardButton('Погода')
    ma.add(p1, p2, p3)
    bot.send_message(message.chat.id, "Выбери что ты хочешь и наслаждайся)", reply_markup=ma)

@bot.message_handler(commands=['kod'])
def start(message):
    ma = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    p99 = types.KeyboardButton('Назад')
    ma.add(p99)
    bot.send_message(message.chat.id, ")))", reply_markup=ma)
    num = sum(1 for line in open('10.json'))
    w = num - 6
    m = bot.send_message(message.chat.id, f'Напиши мне код от 1 до {w}', parse_mode='html')
    bot.register_next_step_handler(m, test)

def test(message):
    y = message.text
    num = sum(1 for line in open('10.json'))
    d = num - 6
    if int(y) <= d:
        with open('10.json', 'r', encoding='utf8') as f:
            s = json.load(f)
            l = str(y)
            for i in range(len(s.get('an'))):
                k = s.get('an')[i]
                bot.send_message(message.chat.id, 'Название: ' + str(k.get(y)) + ' Еще раз /kod')
    else:
        bot.send_message(message.chat.id, 'Еще раз /kod')


@bot.message_handler()
def get_user_text(message):
    if message.text == "Фильмы":
        ma = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        p5 = types.KeyboardButton('Рандом фильм')
        p7 = types.KeyboardButton('Фильм по коду')
        p99 = types.KeyboardButton('Назад')
        ma.add(p5, p7, p99)
        bot.send_message(message.chat.id, "Ой фильмы ихихихих", reply_markup=ma)

    if message.text == "Картинки":
        ma = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        p8 = types.KeyboardButton('Рандом дед инсайд')
        p10 = types.KeyboardButton('рандом ава')
        p99 = types.KeyboardButton('Назад')
        ma.add(p8, p10, p99)
        bot.send_message(message.chat.id, "Ой картинки ихихих", reply_markup=ma)

    if message.text == "Погода":
        ma = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        p55 = types.KeyboardButton('дай погоду')
        p99 = types.KeyboardButton('Назад')
        ma.add(p55, p99)
        bot.send_message(message.chat.id, "Ой погода", reply_markup=ma)

    if message.text == "дай погоду":
        bot.send_message(message.from_user.id, "Введите название города")
        bot.register_next_step_handler(message, get_weather)

    if message.text == "Рандом дед инсайд":
        i = "C:/Users/60kar/Desktop/Bot/ded"
        f = os.listdir(i)
        g = len(f)
        c = random.randint(1, g)
        photo = Image.open("C:/Users/60kar/Desktop/Bot/ded/" + str(c) + '.jpg')
        bot.send_photo(message.chat.id, photo, 'ой вырубай')

    if message.text == "рандом ава":
        i = "C:/Users/60kar/Desktop/Bot/ava"
        f = os.listdir(i)
        g = len(f)
        c = random.randint(1, g)
        photo = Image.open("C:/Users/60kar/Desktop/Bot/ava/" + str(c) + '.jpg')
        bot.send_photo(message.chat.id, photo, 'ну как тебе ава')

    if message.text == "Рандом фильм":
        num = sum(1 for line in open('film1.json'))
        with open('film1.json', 'r', encoding='utf8') as f:
            s = json.load(f)
            ho = num - 6
            c = random.randint(1, ho)
            l = str(c)
            for i in range(len(s.get('film'))):
                k = s.get('film')[i]
                bot.send_message(message.chat.id, 'Название: ' + str(k.get(l)))

    if message.text == "Фильм по коду":
        bot.send_message(message.chat.id, 'Используйте для это команду /kod')


    if message.text == "Назад":
        ma = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        p1 = types.KeyboardButton('Фильмы')
        p2 = types.KeyboardButton('Картинки')
        p3 = types.KeyboardButton('Погода')
        ma.add(p1, p2, p3)
        bot.send_message(message.chat.id, "Выбери что ты хочешь и наслаждайся)", reply_markup=ma)

def get_weather(message):
    city=message.text
    try:
        w=weather(city)
        bot.send_message(message.from_user.id, f"В городе {city} сейчас {round( w[0]['temp'] ) } градусов, "f" чувствуется как {round(w[0]['feels_like'])} градусов. Чтобы проверить другой город напиши дай погоду)")
    except Exception:
        bot.send_message(message.from_user.id, "Такого города нет в базе")
        bot.send_message(message.from_user.id,"Введите название города")
        bot.register_next_step_handler(message, get_weather)

bot.polling(none_stop=True)
