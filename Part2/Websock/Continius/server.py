""" WebSockets — з постійним з'єднанням

Ми створимо три різні скрипти.

consumer.py — який буде слухати та отримувати повідомлення від сервера Websocket
producer.py — який надсилає повідомлення на сервер
server.py — власне сам Websocket сервер, який пам'ятатиме про свої підключення

Server

​Інтерес для нас представляє сервер. Він є класом Server, який поєднує весь функціонал сервера.
Цей сервер розсилає повідомлення, надіслані producer, всім слухачам consumer.

Екземпляр класу Server має асинхронну функцію ws_handler, яка і визначає співпрограму оброблювача
веб-сокета. При підключенні клієнта, функція ws_handler приймає з'єднання, створює екземпляр ws
класу WebSocketServerProtocol і здійснює "рукостискання" (handshake). Далі ми запам'ятовуємо
екземпляр клієнта за допомогою функції register і поміщаємо його у змінну класу clients, яка є
множиною. Як тільки обробник завершує роботу, нормально або за винятком WebSocketProtocolError,
сервер виконує закриваюче "рукостискання" та закриває з'єднання, і видаляє дані про клієнта за
допомогою функції unregister.

Запуск сервера призведе до виконання співпрограми main, яка запустить веб-сокет server.ws_handler.
Наш метод ws_handler реєструє з'єднання await self.register(ws), відправляє повідомлення
підключеним клієнтам await self.distrubute(ws) і, нарешті, закриває з'єднання
await self.unregister(ws).

Нагадаємо, що consumer залишається підключеним до сервера, у той час як producer скасовує власну
реєстрацію.

INFO
Відключення від сервера призведе до помилки ConnectionClosedOK. Сервер чекає наступного
повідомлення з recv(), коли клієнт вимкнувся. Коли це відбувається, websockets підіймає виняток
ConnectionClosedOK, щоб ви знали, що ви не отримаєте інше повідомлення по цьому з'єднанні.
Тому обробляємо його як рекомендує документація.

Метод distribute надсилатиме кожне повідомлення у веб-сокеті всім клієнтам у списку підключених
клієнтів clients.

Запуск

​Запустимо сервер і ми повинні побачити наступне виведення:

INFO:websockets.server:server listening on 127.0.0.1:4000
INFO:websockets.server:server listening on [::1]:4000

Запускаємо 'consumer.py' у нього поки немає жодного виведення в термінал, а у сервера бачимо
нове виведення:

INFO:websockets.server:connection open
INFO:root:('::1', 53648, 0, 0) connects

Це означає, що consumer успішно з'єднався із сервером і чекає на повідомлення. Сервер зберіг
з'єднання consumer у властивість clients.

Запускаємо producer командою:

# py .\produce.py 'Hi all!'

У терміналі consumer ми побачимо отримане повідомлення:

INFO:root:Message: Hi all!

У сервера з'явиться запис у логах, що producer приєднався, відправив повідомлення та успішно
закрив з'єднання:

INFO:websockets.server:connection open
INFO:root:('::1', 53657, 0, 0) connects
INFO:root:('::1', 53657, 0, 0) disconnects
INFO:websockets.server:connection closed
"""

import asyncio
import logging
import websockets

from websockets.legacy.server import WebSocketServerProtocol
# .legacy.server.WebSocketServerProtocol є підкласом .server.ServerProtocol, який є підкласом
# .protocol.Protocol. У документації рекомендується використовувати
# .legacy.server.WebSocketServerProtocol, оскільки він має кращу підтримку для старих версій Python
# і не використовує нові функції, які можуть бути недоступні в деяких середовищах. Якщо ви
# використовуєте Python 3.7 або новішу версію, ви можете використовувати .server.ServerProtocol
# без проблем, але .legacy.server.WebSocketServerProtocol є більш сумісним варіантом для широкого
# спектру середовищ.

from websockets.exceptions import ConnectionClosedOK
# ConnectionClosedOK є винятком, який піднімається, коли клієнт закриває з'єднання. Це дозволяє
# серверу обробляти ситуацію, коли клієнт відключається, без винятків, які можуть порушити роботу
# сервера.

logging.basicConfig(level=logging.INFO)


class Server:
    """ Сервер Websocket, який розсилає повідомлення всім підключеним клієнтам."""
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        """ Реєструє клієнта, додаючи його до множини clients."""
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        """ Видаляє клієнта з множини clients."""
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        """ Надсилає повідомлення всім підключеним клієнтам."""
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        """ Обробник веб-сокета, який реєструє клієнта, розсилає повідомлення та видаляє клієнта
        при відключенні."""
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        """ Розсилає повідомлення всім клієнтам, отримуючи їх від поточного клієнта."""
        async for message in ws:
            await self.send_to_clients(message)


async def main():
    """ Запускає сервер Websocket на localhost:4000."""
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 4000):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
