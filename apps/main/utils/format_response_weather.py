from datetime import datetime


def format_response_weather(weather: dict):
    weather['daily']['time'] = [datetime.strptime(
        day, '%Y-%m-%d') for day in weather['daily']['time']]

    weather['avg'] = [
        {
            'day': weather['daily']['time'][i],
            'temperature': (weather['daily']['temperature_2m_max'][i] +
                            weather['daily']['temperature_2m_min'][i]) / 2,
        }
        for i in range(len(weather['daily']['time']))
    ]

    return weather
