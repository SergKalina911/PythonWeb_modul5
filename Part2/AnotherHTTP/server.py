""" Запити іншими методами HTTP

​Поки що ми виконували тільки GET запити, але документація наводить приклади відправлення для
інших методів HTTP:

        session.post('http://httpbin.org/post', data=b'data')
        session.put('http://httpbin.org/put', data=b'data')
        session.delete('http://httpbin.org/delete')
        session.head('http://httpbin.org/get')
        session.options('http://httpbin.org/get')
        session.patch('http://httpbin.org/patch', data=b'data')

Розглянемо приклад відправлення POST запиту. Спочатку створимо найпростіший Web-сервер
(він працює на порту 5000 і просто відправить рядок 'Done request!' і додасть набір даних,
які ми йому відправимо в POST запиті.),який прийматиме і надсилатиме назад дані POST запиту: """

from http.server import HTTPServer, BaseHTTPRequestHandler
# HTTPServer - клас для створення HTTP сервера
# BaseHTTPRequestHandler - базовий клас для обробки HTTP запитів


class HttpHandler(BaseHTTPRequestHandler):
    """ Обробник HTTP запитів, який приймає POST запити і відповідає на GET запити. """
    def do_POST(self):
        """ Обробник POST запиту, який читає дані з запиту і надсилає їх назад у відповіді. """
        data = self.rfile.read(int(self.headers['Content-Length']))
        print(data)
        self.send_response(201)
        self.end_headers()
        self.wfile.write(b'Done request!' + data)

    def do_GET(self):
        """ Обробник GET запиту, який відповідає на нього простим повідомленням. """
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')


def run(server_class=HTTPServer, handler_class=HttpHandler):
    """ Запускає HTTP сервер на порту 5000. """
    server_address = ('', 5000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()

# Вивід у консолі після відправлення POST запиту з даними 'message=Hello+world%21':
# 127.0.0.1 - - [31/Oct/2022 16:29:15] "POST / HTTP/1.1" 201 - b'message=Hello+world%21'
