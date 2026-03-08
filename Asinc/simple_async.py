""" Основи роботи з asyncio
Щоб функція виконувалася в асинхронному режимі та виступала в ролі coroutine, перед її 
визначенням необхідно додати ключове слово async.

У модулі asyncio є функція run, яка створює Event loop, поміщає у чергу передану coroutine
і, коли черга спорожніє, завершує Event loop. Ви можете зробити всі ці операції самостійно,
якщо потрібно, але бажаний спосіб — run.

Це найпростіший приклад на async/await. Виклик print(r) нам повертає об'єкт coroutine.
Щоб отримати результат від асинхронної функції baz, нам потрібен await. І тільки виконавши
result = await r, ми отримаємо у змінній result значення Hello world."""

import asyncio


async def bazz() -> str:
    """ Приклад асинхронної функції, яка виконує затримку в 1 секунду і повертає рядок 
    'Hello world'."""
    print('Before Sleep')
    await asyncio.sleep(1)
    print('After Sleep')
    return 'Hello world'


async def main():
    """ Головна асинхронна функція, яка викликає bazz і виводить результат. Спочатку
    вона викликає baz і виводить об'єкт coroutine, потім очікує результат за допомогою 
    await і виводить його."""
    r = bazz()
    print(r)
    result = await r
    print(result)


if __name__ == '__main__':
    asyncio.run(main())


# Отримаємо ми наступне виведення:
# <coroutine object bazz at 0x00000211E82CCDD0>
# Before Sleep
# After Sleep
# Hello world
