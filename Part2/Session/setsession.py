""" Набір параметрів сесії

​Кожен об'єкт ClientSession може бути індивідуально налаштований, щоб усі запити у цій сесії
використовували загальний набір параметрів. Для цього ви можете передати в сесію набір параметрів
запиту і всі вони будуть автоматично додані у кожен запит цієї сесії. У цьому прикладі всім запитам
у цій сесії встановили в заголовок поле Request-Id та таймаут на читання 1 секунди."""

import platform
# Цей імпорт потрібен для того, щоб встановити правильну політику циклу подій на Windows.
import asyncio
# Цей імпорт потрібен для того, щоб використовувати асинхронні функції та керувати циклом подій.
from uuid import uuid4
# Цей імпорт потрібен для того, щоб генерувати унікальні ідентифікатори для заголовка Request-Id.
import aiohttp
# Цей імпорт потрібен для того, щоб використовувати бібліотеку aiohttp для виконання асинхронних
# HTTP-запитів.

async def main():
    """ Створюємо сесію з набором параметрів, який включає заголовок Request-Id та таймаут на
    читання 1 секунду."""
    timeout = aiohttp.ClientTimeout(total=1)
    async with aiohttp.ClientSession(
        headers={"Request-Id": str(uuid4())},
        timeout=timeout,
    ) as session:
        async with session.get('https://python.org') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            return f"Body: {html[:15]}..."


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)

# Виведення прикладу:
# Status: 200
# Content-type: text/html; charset=utf-8
# Body: <!doctype html>...
