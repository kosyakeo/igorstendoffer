import telebot
import json
import requests
import random

API = "8017958123:AAGSB6UFz7Z_Ho_1BBLTD-fuSc9-XFULKbo"
WEATHER_API_KEY = "3cac73d629c89471a26530853557dec4"
bot = telebot.TeleBot(API)

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
        response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
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

keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row("кота на базу", "шабаку на базу")
keyboard.row("тачку на базу", "население страны")
keyboard.row("расскажи шутку", "погода")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, text="здравствуй", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "кота на базу")
def send_cat(message):
    image = get_cat_image_url()
    bot.send_photo(message.chat.id, photo=image)

@bot.message_handler(func=lambda message: message.text == "шабаку на базу")
def send_dog(message):
    image = get_dog_image_url()
    bot.send_photo(message.chat.id, photo=image)

@bot.message_handler(func=lambda message: message.text == "тачку на базу")
def send_car(message):
    image = get_car_image_url()
    if image:
        bot.send_photo(message.chat.id, photo=image)
    else:
        bot.send_message(message.chat.id, text="Извини, не могу найти фото тачки сейчас.")

@bot.message_handler(func=lambda message: message.text == "население страны")
def ask_for_country(message):
    bot.send_message(message.chat.id, "Введите название страны на английском (например: Russia)")
    bot.register_next_step_handler(message, process_country_population)

@bot.message_handler(func=lambda message: message.text == "расскажи шутку")
def tell_joke(message):
    joke = get_random_joke()
    bot.send_message(message.chat.id, joke)

@bot.message_handler(func=lambda message: message.text == "погода")
def ask_for_city(message):
    msg = bot.send_message(message.chat.id, "В дубайск захотел? Ладно вводи городок")
    bot.register_next_step_handler(msg, show_weather)

def show_weather(message):
    city = message.text.strip()
    weather = get_weather(city)
    
    if weather:
        response = f"Сейчас в городе {weather['city']}:\n {weather['temp']}°C (ощущается как {weather['feels_like']}°C)"
        bot.send_message(message.chat.id, response, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Че ввел, сам хоть понял?", reply_markup=keyboard)

def process_country_population(message):
    country = message.text.strip()
    population = get_country_population(country)
    if population:
        bot.reply_to(message, f"Население страны {country}: {population} человек")
    else:
        bot.reply_to(message, "Не удалось найти данные. Проверьте название страны.")

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    # Проверяем, не является ли сообщение ответом на предыдущий запрос
    if not (message.reply_to_message and 
           (message.reply_to_message.text == "В каком городе показать температуру?" or 
            message.reply_to_message.text == "Введите название страны на английском (например: Russia)")):
        
        # Если сообщение похоже на название города (первая буква заглавная)
        if message.text and message.text[0].isupper():
            weather = get_weather(message.text)
            if weather:
                show_weather(message)
                return
        
        bot.reply_to(message, "Используйте кнопки меню или введите название города")

bot.infinity_polling()