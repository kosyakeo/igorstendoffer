import telebot
import json
import requests
import random
from telebot import types
API = "8017958123:AAGSB6UFz7Z_Ho_1BBLTD-fuSc9-XFULKbo"
WEATHER_API_KEY = "3cac73d629c89471a26530853557dec4"
GIPHY_API_KEY = "Z5DSUwBMYhG914dP2TPFVnICvM2mRmRa"
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

def get_random_gif():
    try:
        response = requests.get(f'https://api.giphy.com/v1/gifs/random?api_key={GIPHY_API_KEY}&rating=g')
        if response.status_code == 200:
            data = json.loads(response.text)
            return data['data']['images']['original']['url']
    except:
        return None
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
    
def create_main_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton("🐱 Котик", callback_data="cat"),
        types.InlineKeyboardButton("🐶 Собачка", callback_data="dog")
    )
    keyboard.row(
        types.InlineKeyboardButton("🚗 Машина", callback_data="car"),
        types.InlineKeyboardButton("🎬 Гифка", callback_data="gif")
    )
    keyboard.row(
        types.InlineKeyboardButton("🌍 Население страны", callback_data="population"),
        types.InlineKeyboardButton("😂 Шутка", callback_data="joke")
    )
    keyboard.row(
        types.InlineKeyboardButton("☀️ Погода", callback_data="weather"),
        types.InlineKeyboardButton("🔄 Сброс", callback_data="reset")
    )
    return keyboard

def create_back_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("◀️ Назад")
    return keyboard

@bot.message_handler(commands=['start', 'reset'])
def welcome(message):
    bot.send_message(
        message.chat.id,
        text="Привет! Выбери что тебе нужно:",
        reply_markup=create_main_keyboard()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "cat":
        image = get_cat_image_url()
        bot.send_photo(call.message.chat.id, photo=image)
        show_main_menu(call.message)
    elif call.data == "dog":
        image = get_dog_image_url()
        bot.send_photo(call.message.chat.id, photo=image)
        show_main_menu(call.message)
    elif call.data == "car":
        image = get_car_image_url()
        if image:
            bot.send_photo(call.message.chat.id, photo=image)
        else:
            bot.send_message(call.message.chat.id, "Извини, не могу найти фото машины сейчас.")
        show_main_menu(call.message)
    elif call.data == "gif":
        gif_url = get_random_gif()
        if gif_url:
            bot.send_animation(call.message.chat.id, animation=gif_url)
        else:
            bot.send_message(call.message.chat.id, "Не удалось загрузить гифку. Попробуйте позже.")
        show_main_menu(call.message)
    elif call.data == "population":
        msg = bot.send_message(
            call.message.chat.id, 
            "Введите название страны (например: Россия)\nИли нажмите '◀️ Назад' для возврата",
            reply_markup=create_back_keyboard()
        )
        bot.register_next_step_handler(msg, process_country_population)
    elif call.data == "joke":
        joke = get_random_joke()
        bot.send_message(call.message.chat.id, joke)
        show_main_menu(call.message)
    elif call.data == "weather":
        msg = bot.send_message(
            call.message.chat.id, 
            "Введи название города\nИли нажмите '◀️ Назад' для возврата",
            reply_markup=create_back_keyboard()
        )
        bot.register_next_step_handler(msg, show_weather)
    elif call.data == "reset":
        welcome(call.message)
    
    try:
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
    except:
        pass

def show_main_menu(message):
    bot.send_message(
        message.chat.id,
        text="Выбери что тебе нужно:",
        reply_markup=create_main_keyboard()
    )

def show_weather(message):
    if message.text == "◀️ Назад":
        show_main_menu(message)
        return
        
    city = message.text.strip()
    weather = get_weather(city)
    
    if weather:
        response = f"Сейчас в городе {weather['city']}:\n {weather['temp']}°C (ощущается как {weather['feels_like']}°C)"
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Не удалось получить данные о погоде. Проверьте название города.")
    
    show_main_menu(message)

def process_country_population(message):
    if message.text == "◀️ Назад":
        show_main_menu(message)
        return
        
    country = message.text.strip()
    population = get_country_population(country)
    if population:
        bot.send_message(message.chat.id, f"Население страны {country}: {population} человек")
    else:
        bot.send_message(message.chat.id, "Не удалось найти данные. Проверьте название страны.")
    
    show_main_menu(message)

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    if message.text == "◀️ Назад":
        show_main_menu(message)
        return
        
    if message.text and message.text[0].isupper():
        weather = get_weather(message.text)
        if weather:
            show_weather(message)
            return
        
        population = get_country_population(message.text)
        if population:
            bot.send_message(message.chat.id, f"Население страны {message.text}: {population} человек")
            show_main_menu(message)
            return
    
    bot.send_message(message.chat.id, "Используй кнопки ниже! Я тебя не совсем понял!")
    show_main_menu(message)

bot.infinity_polling()