""" Використання однієї сесії при запитах

​Типовий підхід використовувати одну сесію для з'єднання з одним сервісом — це значно прискорює
виконання кількох запитів на один і той самий сервіс. У такому разі ви можете передавати
створену сесію як аргумент у функцію.

У цьому прикладі ми робимо два запити на один і той самий сервіс, але на різні ресурси. Запити
виконуються "одночасно" та використовують те саме з'єднання (сесію). Таким чином, час виконання
двох запитів буде швидшим і трохи більшим, ніж час виконання найтривалішого із запитів. """

import platform
import asyncio
import aiohttp

async def index(session):
    """ Звертаємося до головної сторінки python.org, використовуючи сесію, передану як аргумент."""
    url = 'https://python.org'
    async with session.get(url) as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])

        html = await response.text()
        return f"Body: {html[:15]}..."


async def doc(session):
    """ Звертаємося до сторінки документації python.org, використовуючи сесію, передану як
    аргумент. Зверніть увагу, що ми використовуємо ту саму сесію, що й у функції index()."""
    url = "https://www.python.org/doc/"
    async with session.get(url) as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])

        html = await response.text()
        return f"Body: {html[:15]}..."


async def main():
    """ Створюємо сесію та передаємо її як аргумент у функції index() та doc(). Використовуємо
asyncio.gather() для виконання обох функцій одночасно. Зверніть увагу, що обидві функції 
використовують одну і ту саму сесію для виконання запитів. """
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(index(session), doc(session))
        return result


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)

# Виведення прикладу:
# Status: 200
# Content-type: text/html; charset=utf-8
# Status: 200
# Content-type: text/html; charset=utf-8
# ['Body: <!doctype html>...', 'Body: <!doctype html>...']
