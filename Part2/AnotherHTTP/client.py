""" Клієнт для відправлення HTTP запитів """

import platform
import asyncio
from uuid import uuid4
import aiohttp

async def main():
    """ Головна функція, яка відправляє POST запит на локальний сервер і виводить статус та тіло
    відповіді. Використовує бібліотеку aiohttp для асинхронного HTTP клієнта."""
    async with aiohttp.ClientSession() as session:
        # Відправляємо POST запит на локальний сервер з даними у вигляді словника
        # {"message": "Hello world!"} і вимикаємо SSL перевірку (ssl=False) для локального сервера
        async with session.post('http://localhost:5000', data={"message": "Hello world!"}, ssl=False) as response:

            print("Status:", response.status)
            html = await response.text()
            return f"Body: {html}"


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)

# Вивід у консолі після відправлення POST запиту:
# Status: 201
# Body: Done request!message=Hello+world%21
