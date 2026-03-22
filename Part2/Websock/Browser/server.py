""" WebSockets робота з браузером

Спочатку створимо сервер за аналогією до попереднього прикладу.
Тут нам уже все знайоме, ми отримуємо дані, далі додаємо перед ними рядок Data recieved as:
і відправляємо назад клієнту. Різниця в тому, що сервер веб-сокет працює на 8000 порту.

Клієнт цього разу у нас буде на javascript вбудований всередину html файлу."""

import asyncio
import websockets


async def handler(websocket):
    """ Обробник для веб-сокетів, який отримує дані від клієнта, формує відповідь і відправляє
    її назад.   """
    data = await websocket.recv()
    reply = f"Data recieved as:  {data}!"
    print(reply)
    await websocket.send(reply)


async def main():
    async with websockets.serve(handler, "localhost", 8000):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
