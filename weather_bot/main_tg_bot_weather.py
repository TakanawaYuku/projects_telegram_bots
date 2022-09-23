from email import message
import requests
from datetime import datetime as dt
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(
        f'Привет напиши название своего города и я пришлю тебе сводку погоды!')


@dp.message_handler()
async def get_weather(message: types.Message):

    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F326',
        'Mist': 'Туман \U0001F32B'
    }

    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric'
        )
        data = r.json()

        local_city = data['name']
        cur_weather = data['main']['temp']
        weather_description = data['weather'][0]['main']

        if weather_description in code_to_smile:
            weather = code_to_smile[weather_description]
        else:
            weather = 'Посмотри в окно'

        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        sunrise_timestamp = dt.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = dt.fromtimestamp(data['sys']['sunset'])

        await message.reply(
            f'***{dt.now().strftime("%Y-%m-%d %H:%M")}***\n'
            f'Погода в городе: {local_city}\nТемпература: {round(cur_weather)}℃\nВлажность: {humidity}%\nПогода: {weather}\nВетер: {wind}м/с\n'
            f'Рассвет: {sunrise_timestamp}\n'
            f'Закат: {sunset_timestamp}\n'
            f'Хорошего дня!')

    except:
        await message.reply('\U00002620 Проверьте название города \U00002620')


if __name__ == '__main__':
    executor.start_polling(dp)
