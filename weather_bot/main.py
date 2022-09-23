from config import open_weather_token
import requests
from datetime import datetime as dt


def get_weather(city, open_weather_token):

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
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric'
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



        print(
            f'***{dt.now().strftime("%Y-%m-%d %H:%M")}***\n'
            f'Погода в городе: {local_city}\nТемпература: {round(cur_weather)}℃\nВлажность: {humidity}%\nПогода: {weather}\nВетер: {wind}м/с\n'
            f'Рассвет: {sunrise_timestamp}\n'
            f'Закат: {sunset_timestamp}\n'
            f'Хорошего дня!')

    except Exception as ex:
        print(ex)
        print('Проверьте название города')


def main():
    city = input('Введите ваш город: ').capitalize()
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()
