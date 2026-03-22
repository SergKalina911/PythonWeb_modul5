""" WebSockets — з постійним з'єднанням

Ми створимо три різні скрипти.

consumer.py — який буде слухати та отримувати повідомлення від сервера Websocket
producer.py — який надсилає повідомлення на сервер
server.py — власне сам Websocket сервер, який пам'ятатиме про свої підключення 

Спочатку створимо простого споживача повідомлень від Websocket сервера consumer.py
Тут за допомогою функції consumer ми підключаємося до віддаленого Websocket сервера на порту 4000.
Як і раніше, через асинхронний контекст підключення, отримуємо екземпляр ws класу
WebSocketClientProtocol:

    async with websockets.connect(ws_resource_url) as ws:

Далі за допомогою асинхронного циклу async for ми виконуватимемо перебір асинхронного ітератора
ws і логуємо отримані повідомлення.

    async for message in ws:
        logging.info(f"Message: {message}") """

import asyncio
import logging
import websockets

logging.basicConfig(level=logging.INFO)


async def consumer(hostname: str, port: int):
    """ Підключаємось до віддаленого Websocket сервера на порту 4000. Через асинхронний
    контекст підключення отримуємо екземпляр ws класу WebSocketClientProtocol. Далі за
    допомогою асинхронного циклу async for виконуємо перебір асинхронного ітератора ws і
    логуватимемо отримані повідомлення. """
    ws_resource_url = f"ws://{hostname}:{port}"
    async with websockets.connect(ws_resource_url) as ws:
        async for message in ws:
            logging.info(f"Message: {message}")


if __name__ == '__main__':
    asyncio.run(consumer('localhost', 4000))

