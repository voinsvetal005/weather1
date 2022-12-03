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

f = open('december.txt', 'r', encoding='UTF-8')
jokes = f.read().split('\n')
f.close()
# Пока не закончатся шутки, посылаем их в канал

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
    for joke in jokes:
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
                wd = "Неясно"

            humidity = data["main"]["humidity"]
            pressure = int(data["main"]["pressure"]/1.33)
            wind = data["wind"]["speed"]

            soros = joke.split('*')
            
            await bot.send_photo(channel_id, soros[1], caption=f"Сегодня {datetime.datetime.now().strftime('%d-%m-%Y')}.\nДо Нового года {formaslova2}... {d.days} {formaslova1}!\n"
              f"Погода в Лосином острове сейчас: \nТемпература: {cur_weather} C° {wd}\n"
              f"Влажность: {humidity}%  Давление: {pressure} мм.рт.ст  Ветер: {wind} м/с\n\n"
              f"_{soros[0]}_", parse_mode="Markdown" 
              )
            time.sleep(30)
            
        except:
            await message.reply("\U00002620 Проверьте название города \U00002620")
if __name__ == '__main__':
    executor.start_polling(dp)