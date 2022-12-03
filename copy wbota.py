import requests
import datetime
import schedule, time
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


#def send_messange():
    # ваша функция отправки сообщений    
channel_id = '-1001830691651' #Пробабота
#channel_id = '-1001623252716' #Заповедные


#channel_id = '-1001162004912' #Лосиный
bot = Bot(token=tg_bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

gorod='Mytishchi'
#gorod='Moscow'
now = datetime.datetime.today()
NY = datetime.datetime(2023,1,2)
d = NY-now #  str(d)  '83 days, 2:43:10.517807'

formaslova1 = "дней"
formaslova2 = "осталось"
d1 = {1,21,31} 
d2 = {2,3,4,22,23,24}

if d.days in d1:
    formaslova1 ="день"
    formaslova2 ="остался"
else: 
    if d.days in d2:
        formaslova1 ="дня"

#@dp.message_handler(commands=["start"])
#async def start_command(message: types.Message):
#    await message.reply("Привет! Напиши мне что угодно и я пришлю сводку погоды в Лосином острове!")
code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
    }

@dp.message_handler()
async def get_weather(message: types.Message):
    #code_to_smile = {
    #    "Clear": "Ясно \U00002600",
    #    "Clouds": "Облачно \U00002601",
    #    "Rain": "Дождь \U00002614",
    #    "Drizzle": "Дождь \U00002614",
    #    "Thunderstorm": "Гроза \U000026A1",
    #    "Snow": "Снег \U0001F328",
    #    "Mist": "Туман \U0001F32B"
    #}
    #code_to_smile = {
    #    "Clear": "\U00002600",
    #    "Clouds": "\U00002601",
    #    "Rain": "\U00002614",
    #    "Drizzle": "\U00002614",
    #    "Thunderstorm": "\U000026A1",
    #    "Snow": "U0001F328",
    #    "Mist": "U0001F32B"
    #}

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={gorod}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = int(data["main"]["pressure"]/1.33)
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        

        #await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
        #      f"Погода в Лосином острове: \nТемпература: {cur_weather}C° {wd}\n"
        #      f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
        #      f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
        #      f"***Хорошего дня!***"
        #      )
        #await bot.send_message(channel_id, f"Сегодня {datetime.datetime.now().strftime('%d-%m-%Y')}. " #f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              #f"До Нового года осталось 30 дней!\n"
              #f"в ЛО: {cur_weather}C° {wd} "
              #f"Погода в Лосином острове: \nТемпература: {cur_weather} C° {wd}\n"
              #f"Вет: {wind} м/с Вл: {humidity}% Дав: {pressure} мм.\n\n"
              #f"Влажность: {humidity}%  Давление: {pressure} мм.рт.ст  Ветер: {wind} м/с\n\n"
              #f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n\n"
            
              #f"Декабрь – стужайло на всю зиму землю студит. Он и замостит, и загвоздит, и саням ход даст!"
              #)
        await bot.send_photo(channel_id, 'https://photos.app.goo.gl/LN4QFvzdd9BVqo6r9', caption=f"Сегодня {datetime.datetime.now().strftime('%d-%m-%Y')}.\nДо Нового года {formaslova2}... {d.days} {formaslova1}!\n"
              f"Погода в Лосином острове сейчас: \nТемпература: {cur_weather} C° {wd}\n"
              f"Влажность: {humidity}%  Давление: {pressure} мм.рт.ст  Ветер: {wind} м/с\n\n"
              f"_Если в этот день выпало много снега, зима будет снежной и морозной. Говорили, что снег, выпавший 4 декабря, может пролежать до весны. И наоборот - морозный, бесснежный и солнечный день 4 декабря означает, что зима будет мягкая и относительно тёплая._", parse_mode="Markdown" 
              )
    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")
        
#schedule.every().day.at("12:32").do(send_messange)
#while True: # этот цикл отсчитывает время. Он обязателен.
#    schedule.run_pending()
#    time.sleep(1)

if __name__ == '__main__':
    executor.start_polling(dp)