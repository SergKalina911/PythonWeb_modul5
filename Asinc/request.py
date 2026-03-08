""" Паралельне виконання IO-bound завдань

Так само можна перетворити на паралельне виконання мережеві запити requests. Спочатку 
запустимо синхронний код, а потім перетворимо його на асинхронний, використовуючи за 
допомогою пакету concurrent.futures.

Ми робимо функцію обгортку preview_fetch_async над функцією preview_fetch. Всередині 
беремо поточний виконуваний Event loop loop = asyncio.get_running_loop() та за допомогою 
ThreadPoolExecutor поміщаємо функцію preview_fetch в 
Executor - [loop.run_in_executor(pool, preview_fetch, url) for url in urls]. 
Отриманий список об'єктів Futures передаємо в asyncio.gather(*futures) для отримання 
остаточного результату.

NOTE
Параметр 'return_exceptions' відповідає за обробку помилок, за замовчуванням встановлено 
значення False. Перший згенерований виняток негайно поширюється на завдання, що очікує в 
gather. Якщо return_exceptions має значення True, винятки обробляються так само, як і 
успішні результати, та об'єднуються у списку результатів.

Як бачимо, навіть за такої малої кількості запитів, ми бачимо приріст продуктивності при 
виконанні async/await операцій."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from time import time, sleep
import requests

urls = ['http://www.google.com', 'http://www.python.org', 'http://duckduckgo.com']


def preview_fetch(url_to_fetch):
    """ Функція preview_fetch виконує синхронний запит до веб-сайту за допомогою 
    requests.get. Вона приймає URL-адресу як аргумент, виконує запит і повертає кортеж,
    що містить URL-адресу та перші 150 символів відповіді. Ця функція є синхронною і буде
    блокувати виконання, поки не отримає відповідь від сервера. """
    response = requests.get(url_to_fetch, timeout=10)
    return url_to_fetch, response.text[:150]


async def preview_fetch_async():
    """ Функція preview_fetch_async є асинхронною обгорткою над функцією preview_fetch.
    Вона використовує ThreadPoolExecutor для виконання функції preview_fetch у фоновому потоці.
    Всередині функції ми отримуємо поточний виконуваний Event loop за допомогою 
    asyncio.get_running_loop(), створюємо ThreadPoolExecutor з 3 потоками і запускаємо функцію
    preview_fetch для кожного URL в списку urls за допомогою loop.run_in_executor. Результати
    виконання зберігаються у списку futures, який потім передається в asyncio.gather для отримання
    остаточного результату. Якщо під час виконання виникають винятки, вони обробляються і
    повертаються разом з успішними результатами."""
# Отримуємо поточний виконуваний Event loop, який відповідає за управління асинхронними задачами.
    loop = asyncio.get_running_loop()
    # Створюємо ThreadPoolExecutor з 3 потоками, який дозволяє виконувати функцію preview_fetch
    # у фоновому потоці. Це дозволяє нам виконувати синхронні запити до веб-сайтів без блокування
    # основного потока.
    with ThreadPoolExecutor(3) as pool:
        # Запускаємо функцію preview_fetch для кожного URL в списку urls за допомогою
        # loop.run_in_executor.
        # Це дозволяє нам виконувати запити до веб-сайтів паралельно, не блокуючи основний потік.
        # Результати виконання зберігаються у списку futures.
        futures = [loop.run_in_executor(pool, preview_fetch, url) for url in urls]
        # Передаємо список об'єктів Futures в asyncio.gather для отримання остаточного результату.
        # Якщо під час виконання виникають винятки, вони обробляються і повертаються разом з
        # успішними результатами.
        result = await asyncio.gather(*futures, return_exceptions=True)
        return result


if __name__ == '__main__':
    # Синхронна частина коду, яка виконує послідовні запити до веб-сайтів. Ми вимірюємо
    # час виконання, запускаючи функцію preview_fetch для кожного URL в списку urls.
    # Після отримання результату ми виводимо його в консоль разом з часом виконання.
    # Ви побачите, що запити виконуються послідовно, і загальний час виконання буде
    # більшим, ніж якщо б ми виконували їх паралельно.
    start = time()
    for url in urls:
        r = preview_fetch(url)
        print(r)
    print(time() - start)
    # Асинхронна частина коду, яка виконує паралельні запити до веб-сайтів. Ми вимірюємо
    # час виконання, запускаючи функцію preview_fetch_async за допомогою asyncio.run.
    # Після отримання результату ми виводимо його в консоль разом з часом виконання.
    # Ви побачите, що запити виконуються паралельно, і загальний час виконання буде меншим,
    # ніж якщо б ми виконували їх послідовно.
    sleep(3)
    print("___"*20)
    print('Async version')
    print("___"*20)
    start = time()
    r = asyncio.run(preview_fetch_async())
    print(r)
    print(time() - start)
