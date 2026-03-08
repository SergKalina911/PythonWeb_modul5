""" Асинхронна робота з файлами

Пакет aiofile дозволяє виконувати асинхронні операції з файлами.
Він підтримує як читання, так і запис файлів, а також надає можливість працювати з файлами
в асинхронному режимі. Треба встановити пакет командою `pip install aiofile` для Python.

Для асинхронної роботи з файлами існує низка пакетів. І почнемо ми з aiofile. Він виконує
асинхронні операції за підтримки пакета asyncio.

Замість звичної функції open, необхідно використовувати async_open. Він повертає файлоподібні
об'єкти python з асинхронними методами.

Методи, що підтримуються:

    - async def read(length = -1) - читання фрагмента з файлу, за довжини -1 файл буде прочитаний
    до кінця.
    - async def write(data) - записати фрагмент у файл
    - def seek(offset) - встановити позицію покажчика файлу
    - def tell() - повертає поточну позицію покажчика файлу
    - async def readline(size=-1, newline="\n") - читати фрагменти до нового рядка або EOF.
    - def __aiter__() -> LineReader - ітератор по рядках.
    - def iter_chunked(chunk_size: int = 32768) -> Reader — ітератор по чанкам.

NOTE
Метод readline неоптимальний для невеликих рядків, оскільки не використовує повторно буфер читання.
Якщо ви хочете читати файл порядково, будь ласка, уникайте використання async_open, замість цього
використовуйте LineReader. """

# Створення файлу "hello.txt" та запис у нього даних за допомогою aiofile

import asyncio
from aiofile import async_open


async def main():
    """ Створюємо файл "hello.txt" та записуємо в нього дані за допомогою aiofile. """
    async with async_open("hello.txt", 'w+') as afp:
        await afp.write("Hello ")
        await afp.write("world\n")
        await afp.write("Hello from - async world!")


# if __name__ == '__main__':
#     asyncio.run(main())

# Підхід await afp.read() дозволяє читати вміст файлу після його запису.
async def afpread():
    """ Читаємо вміст файлу "hello.txt" після його створення та запису даних. """
    async with async_open("hello.txt", 'r') as afp:
        print(await afp.read())

# Підхід async for
async def afpfor():
    """ Читаємо вміст файлу "hello.txt" за допомогою асинхронного циклу. """
    async with async_open("hello.txt", 'r') as afp:
        async for line in afp:
            print(line)

# LineReader - це спеціальний клас, який дозволяє читати файл рядок за рядком в асинхронному режимі.
from aiofile import AIOFile, LineReader

async def line_reader():
    """ Читаємо вміст файлу "hello.txt" за допомогою LineReader. """
    async with AIOFile("hello.txt", 'r') as afp:
        reader = LineReader(afp)
        async for line in reader:
            print(line)

if __name__ == '__main__':
    asyncio.run(main())
    asyncio.run(afpread())
    asyncio.run(afpfor())
    asyncio.run(line_reader())

# В результаті виконання цього коду буде створено файл "hello.txt" з наступним вмістом:
# Hello world
# Hello from - async world!

# І буде виведено вміст файлу на екран кілька разів, використовуючи різні методи читання.
