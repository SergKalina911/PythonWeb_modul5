""" WebSockets — з постійним з'єднанням

Ми створимо три різні скрипти.

consumer.py — який буде слухати та отримувати повідомлення від сервера Websocket
producer.py — який надсилає повідомлення на сервер
server.py — власне сам Websocket сервер, який пам'ятатиме про свої підключення


Producer

​Відправлятимемо повідомлення за допомогою producer. Ми підключаємося до веб-сокету так само,
як робили це раніше з consumer. А далі відправляємо асинхронне повідомлення на сервер
await ws.send(message) та відключаємося."""
import sys
import asyncio
import websockets

async def producer(message: str, host: str, port: int):
    """ Підключаємося до веб-сокету так само, як робили це раніше з consumer. А далі
    відправляємо асинхронне повідомлення на сервер await ws.send(message) та відключаємося"""
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)


if __name__ == '__main__':
    asyncio.run(producer(message=sys.argv[1], host='localhost', port=4000))
