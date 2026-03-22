"""                      Робота із сесіями Aiohttp клієнта

Створення сесій

​У розглянутих раніше прикладах використовуються менеджери контексту, щоб у будь-якому випадку
коректно завершити всі з'єднання та повернути системні ресурси. Це рекомендований підхід і варто
використовувати його скрізь, де це можливо.

Однак, ви також можете створювати сесію та закривати її так, як вам зручно:"""

import platform
import asyncio
import aiohttp


async def main():
    """ Ця функція є основною корутиною, яка демонструє створення сесії Aiohttp клієнта без
    використання менеджера контексту. Вона створює сесію, виконує GET-запит до вказаної URL-адреси
    (https://python.org), виводить статус відповіді та тип вмісту, отримує текст відповіді,
    закриває відповідь та сесію, і повертає перші 15 символів тіла відповіді. """

# Створюємо сесію Aiohttp клієнта та виконуємо GET-запит до вказаної URL-адреси
    session = aiohttp.ClientSession()
    response = await session.get('https://python.org')

    print("Status:", response.status)
    print("Content-type:", response.headers['content-type'])

    html = await response.text()
    response.close()
# Закриваємо сесію після завершення роботи з нею для звільнення системних ресурсів
    await session.close()
    # повертаємо перші 15 символів тіла відповіді для демонстрації отриманих даних без виведення
    # всього тексту (який може бути дуже великим) у консоль
    return f"Body: {html[:15]}..."


if __name__ == "__main__":
    if platform.system() == 'Windows':
        # На Windows потрібно встановити політику циклу подій, щоб уникнути помилки
        # "RuntimeError: Event loop is closed"
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)

# Виведення прикладу:
# Status: 200
# Content-type: text/html; charset=utf-8
# Body: <!doctype html>...
