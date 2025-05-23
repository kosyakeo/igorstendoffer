import telebot
import json
import requests
import random

API = "8017958123:AAGSB6UFz7Z_Ho_1BBLTD-fuSc9-XFULKbo"
WEATHER_API_KEY = "3cac73d629c89471a26530853557dec4"
bot = telebot.TeleBot(API)
COUNTRIES_TRANSLATION = {
    "россия": "russia",
    "сша": "usa",
    "китай": "china",
    "германия": "germany",
    "франция": "france",
    "великобритания": "united kingdom",
    "италия": "italy",
    "испания": "spain",
    "украина": "ukraine",
    "казахстан": "kazakhstan",
    "беларусь": "belarus",
    "япония": "japan",
    "канада": "canada",
    "бразилия": "brazil",
    "индия": "india",
}

JOKES = [
    "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25!",
    "Как называют IT-специалиста, который не боится работы? Безработный!",
    "Почему Python не может поднять тяжести? Потому что у него нету __strength__!",
    "Что сказал один массив другому? 'Давай не будем тормозить!'",
    "Почему чайник принес на работу зонт? На случай, если пойдет дождь из пакетов!",
    "Какой напиток любят алгоритмы? Алгорит-микс!",
    "Почему бот грустил? Потому что у него не было друзей-байтов!",
    "Что сказал ноль восьмерке? 'Неплохой поясок!'",
    "Почему компьютер плохо спал? У него были проблемы с оперативной памятью!",
    "Как называют собаку-программиста? Дог-транслятор!"
]

def translate_country_name(russian_name):
    """Переводит название страны с русского на английский"""
    lower_name = russian_name.lower()
    return COUNTRIES_TRANSLATION.get(lower_name, russian_name)

def get_cat_image_url():
    response = requests.get('https://api.thecatapi.com/v1/images/search').text
    return json.loads(response)[0]['url']

def get_dog_image_url():
    response = requests.get('https://dog.ceo/api/breeds/image/random').text
    return json.loads(response)['message']

def get_car_image_url():
    response = requests.get('https://api.unsplash.com/search/photos', 
                          params={'query': 'car', 'client_id': 'ILyN0JwXGb3F5ppck3ViRn1r51F2RX9iv8J6FhXkNzE'})
    if response.status_code == 200:
        return json.loads(response.text)['results'][0]['urls']['regular']
    else:
        return None

def get_country_population(country_name):
    try:
        english_name = translate_country_name(country_name)
        response = requests.get(f"https://restcountries.com/v3.1/name/{english_name}")
        if response.status_code == 200:
            data = json.loads(response.text)
            return f"{data[0]['population']:,}"
        return None
    except:
        return None
    
def get_random_joke():
    return random.choice(JOKES)

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        response = requests.get(url)
        data = json.loads(response.text)
        
        if data["cod"] != 200:
            return None
            
        return {
            "city": data["name"],
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"])
        }
    except:
        return None
    
main_keyboard = telebot.types.ReplyKeyboardMarkup(True)
main_keyboard.row("Котик", "Собачка")
main_keyboard.row("Машина", "Население страны")
main_keyboard.row("Шутка", "Погода")

no_keyboard = telebot.types.ReplyKeyboardRemove()

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, text="Привет!", reply_markup=main_keyboard)

@bot.message_handler(func=lambda message: message.text == "Котик")
def send_cat(message):
    image = get_cat_image_url()
    bot.send_photo(message.chat.id, photo=image, reply_markup=main_keyboard)

@bot.message_handler(func=lambda message: message.text == "Собачка")
def send_dog(message):
    image = get_dog_image_url()
    bot.send_photo(message.chat.id, photo=image, reply_markup=main_keyboard)

@bot.message_handler(func=lambda message: message.text == "Машина")
def send_car(message):
    image = get_car_image_url()
    if image:
        bot.send_photo(message.chat.id, photo=image, reply_markup=main_keyboard)
    else:
        bot.send_message(message.chat.id, text="Извини, не могу найти фото машины сейчас.", reply_markup=main_keyboard)

@bot.message_handler(func=lambda message: message.text == "Население страны")
def ask_for_country(message):
    msg = bot.send_message(message.chat.id, "Введите название страны (например: Россия)", reply_markup=no_keyboard)
    bot.register_next_step_handler(msg, process_country_population)

@bot.message_handler(func=lambda message: message.text == "Шутка")
def tell_joke(message):
    joke = get_random_joke()
    bot.send_message(message.chat.id, joke, reply_markup=main_keyboard)

@bot.message_handler(func=lambda message: message.text == "Погода")
def ask_for_city(message):
    msg = bot.send_message(message.chat.id, "Введи название города)", reply_markup=no_keyboard)
    bot.register_next_step_handler(msg, show_weather)

def show_weather(message):
    city = message.text.strip()
    weather = get_weather(city)
    
    if weather:
        response = f"Сейчас в городе {weather['city']}:\n {weather['temp']}°C (ощущается как {weather['feels_like']}°C)"
        bot.send_message(message.chat.id, response, reply_markup=main_keyboard)
    else:
        bot.send_message(message.chat.id, "Не пон", reply_markup=main_keyboard)

def process_country_population(message):
    country = message.text.strip()
    population = get_country_population(country)
    if population:
        bot.send_message(message.chat.id, f"Население страны {country}: {population} человек", reply_markup=main_keyboard)
    else:
        bot.send_message(message.chat.id, "Не удалось найти данные. Проверьте название страны.", reply_markup=main_keyboard)

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    if message.text and message.text[0].isupper():
        weather = get_weather(message.text)
        if weather:
            show_weather(message)
            return
        
        population = get_country_population(message.text)
        if population:
            bot.send_message(message.chat.id, f"Население страны {message.text}: {population} человек", reply_markup=main_keyboard)
            return
    
    bot.send_message(message.chat.id, "Используй кнопки меню! Я тебя не совсем понял!", reply_markup=main_keyboard)

bot.infinity_polling()
