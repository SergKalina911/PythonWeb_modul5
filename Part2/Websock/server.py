""" A simple WebSocket server

Запуск сервера виконується командою asyncio.run(main()). Сама функція main за допомогою
асинхронного контексту створює сервер WebSocket командою websockets.serve(hello, "localhost", 8765)

Аргумент hello – це функція обробник повідомлень між сервером та клієнтом, аргумент `localhost'
визначає хост для сервера, а 8765 – порт, на якому буде встановлено з'єднання.

У функції hello ми отримуємо параметр websocket, що має тип WebSocketServerProtocol. Отримуємо
повідомлення від клієнта за допомогою name = await websocket.recv(), а відправляємо повідомлення
виразом await websocket.send(greeting). Як бачимо, по суті, це ехо-сервер.


INFO
Документація каже, що serve() виконує співпрограму обробки з'єднання hello() один раз для кожного
з'єднання WebSocket. Він закриває з'єднання WebSocket, коли обробник повертається."""

import asyncio
import websockets


async def hello(websocket):
    name = await websocket.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")


async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())

# $ python server.py
# <<< Alice
# >>> Hello Alice!
