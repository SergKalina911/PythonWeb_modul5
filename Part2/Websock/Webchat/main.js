console.log('Hello world!')
// Виконуємо з'єднання до веб-сокету
const ws = new WebSocket('ws://localhost:8080')

// Обробляємо подію submit форми при натисканні кнопки <button type="submit">Send message</button>.
//  Зупиняємо стандартну обробку форми, щоб браузер не надіслав повідомлення самостійно командою
//  e.preventDefault().

// Надсилаємо повідомлення самостійно на сервер командою ws.send(textField.value), де 
// textField.value – значення інпута <input type="text" id="textField"/>. Обнулюємо поле
//  введення командою textField.value = null.
formChat.addEventListener('submit', (e) => {
    e.preventDefault()
    ws.send(textField.value)
    textField.value = null
})
// Виводимо вітальне повідомлення у консоль браузера при з'єднанні з веб-сокетом.
ws.onopen = (e) => {
    console.log('Hello WebSocket!')
}
// Цей код спрацьовує, коли сервер надсилає повідомлення клієнту методом send_to_clients.
//  Він отримує повідомлення від веб-сокету та додає його в DOM дерево веб-сторінки.
ws.onmessage = (e) => {
    console.log(e.data)
    text = e.data

    const elMsg = document.createElement('div')
    elMsg.textContent = text
    subscribe.appendChild(elMsg)
}
