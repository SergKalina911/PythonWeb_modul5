""" Пакет aioshutil: Асинхронний аналог модуля shutil для роботи з файлами та каталогами
в асинхронному коді Python.

Бібліотека aioshutil надає асинхронну версію функції модуля Shutil.

Модуль Shutil є синхронним, та його використання в асинхронних застосунках заблокує
цикл подій і уповільнить роботу застосунку, aioshutil надає асинхронні дружні версії
функцій модуля Shutil.

Пакет aioshutil надає асинхронні версії функцій, таких як copyfile(), copy(), move(), rmtree()
та багато інших. Це дозволяє вам виконувати файлові операції, не блокуючи ваш асинхронний код.

Його можна використовувати для копіювання файлів, переміщення файлів та каталогів, видалення
файлів та каталогів, а також для інших операцій з файлами та каталогами, все в асинхронному режимі.

Треба встановити aioshutil за допомогою pip: pip install aioshutil

Для прикладу, давайте ми створимо папку logs та скопіюємо туди наш файл "hello.txt" """

import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile


async def main():
    """ Створюємо папку logs та копіюємо туди наш файл "hello.txt" """
    apath = AsyncPath("hello.txt")
    if await apath.exists():
        new_path = AsyncPath('logs')
        # Створюємо папку logs, якщо її немає, та копіюємо туди файл "hello.txt"
        await new_path.mkdir(exist_ok=True, parents=True)
        await copyfile(apath, new_path / apath)


if __name__ == '__main__':
    asyncio.run(main())
