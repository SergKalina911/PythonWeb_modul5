""" Створюємо найпростіший чат на WebSockets

Код сервера

​Давайте тепер побудуємо найпростіший веб-чат. За основу візьмемо сервер із попереднього розділу.
Тільки тут ми додали імпорт пакету names, який генеруватиме випадкове ім'я користувачеві в чаті.
При реєстрації веб-сокет з'єднання, в методі register, ми його додаємо в екземпляр 
ws: ws.name = names.get_full_name(). Потім ми використовуємо його, коли надсилаємо повідомлення
всім клієнтам: await self.send_to_clients(f"{ws.name}: {message}")."""

import asyncio
import logging
import websockets
import names
from websockets.legacy.server import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

logging.basicConfig(level=logging.INFO)


class Server:
    """ Клас Server відповідає за реєстрацію та відправку повідомлень клієнтам.
    Він зберігає всі активні веб-сокет з'єднання в множині clients. Коли клієнт підключається,
    він реєструється в методі register, а коли відключається - в методі unregister. Метод
    send_to_clients надсилає повідомлення всім клієнтам, які зараз підключені до сервера.
    Метод ws_handler відповідає за обробку веб-сокет з'єднання та викликає метод distrubute
    для розподілу повідомлень між клієнтами."""
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    """ У функції main ми створюємо екземпляр класу Server та запускаємо веб-сокет сервер на
    localhost:8080. Сервер працюватиме вічно, доки його не зупинять вручну або не виникне
    помилка."""
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
