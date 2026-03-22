""" Тепер розглянемо клієнтську частину.
Тут лише одна функція hello, яка надсилає ім'я на сервер, отримує привітання та закриває з'єднання.

URL ресурсу веб-сокету використовує власну схему, що починається з ws (або wss для безпечного
підключення). Далі йде ім'я хосту та номер порту ws://localhost:8765.

async with websockets.connect('ws://localhost:8765') as websocket:

Наступний рядок відкриває з'єднання із веб-сокетом, використовуючи websockets.connect. Очікування
з'єднання викликає WebSocketClientProtocol, який потім використовується для надсилання та отримання
повідомлень. Цей рядок використовує async with, який працює з асинхронним контекстним менеджером.
З'єднання закривається під час виходу з контексту. Далі йде вже знайоме нам по серверу відправлення
та отримання повідомлень за допомогою await websocket.send(name) і
greeting = await websocket.recv().

Запустимо сервер, а далі виконаємо код клієнта у консолі."""

import asyncio
import websockets


async def hello():
    """ Клієнтська частина, яка надсилає ім'я на сервер, отримує привітання та закриває з'єднання.
    URL ресурсу веб-сокету використовує власну схему, що починається з ws (або wss для безпечного
    підключення). Далі йде ім'я хосту та номер порту ws://localhost:8765.
    async with websockets.connect('ws://localhost:8765') as websocket:"""
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f">>> {name}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


if __name__ == "__main__":
    asyncio.run(hello())

# $ python client.py
# What's your name? Alice
# >>> Alice
# <<< Hello Alice!

