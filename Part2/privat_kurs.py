""" Отримання відповіді сервера

Відповідь сервера завжди гарантовано містить заголовок і він буде доступним, щойно
отримає відповідь. Тіло запиту може бути досить великим (файл великого розміру, потік
даних) та AIOHTTP дає можливість обробити тільки заголовок, щоб вирішити завантажувати
далі тіло запиту чи ні.

Як приклад, давайте зробимо запит на публічне API Приватбанку, щодо поточного курсу валют."""

import platform
import asyncio
import aiohttp

async def main():
    """ Ця функція є основною корутиною, яка виконує асинхронний HTTP-запит до API Приватбанку.
    Вона використовує aiohttp для створення клієнтської сесії та виконання GET-запиту до вказаної
    URL-адреси, яка повертає поточний курс валют у форматі JSON. Функція також виводить статус
    відповіді, тип вмісту, отримані куки та результат запиту у вигляді словника Python. """

    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5') as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            print('Cookies: ', response.cookies)
            print(response.ok)
            result = await response.json()
            return result


if __name__ == "__main__":
    if platform.system() == 'Windows':
        # На Windows потрібно встановити політику циклу подій, щоб уникнути помилки
        # "RuntimeError: Event loop is closed"
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)

# Виведення прикладу:

# Status: 200
# Content-type: application/json; charset=UTF-8
# Cookies:
# True
# [{'ccy': 'USD', 'base_ccy': 'UAH', 'buy': '38.90000', 'sale': '39.40000'},
# {'ccy': 'EUR', 'base_ccy': 'UAH', 'buy': '38.00000', 'sale': '39.00000'},
# {'ccy': 'BTC', 'base_ccy': 'USD', 'buy': '19662.0514', 'sale': '21731.7410'}]
