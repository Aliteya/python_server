import socket
import argparse
from message import HTTP_Request
from message import HTTP_Response

class Client:
    def __init__(self, host, port):
        self.client = socket.socket()
        self.__host = host
        self.__port = port 
        self.client.connect((self.__host, self.__port))
        
        parser = argparse.ArgumentParser(description="HTTP 1.1 клиент.")
        parser.add_argument("method", type=str, help="HTTP метод (GET, POST, OPTIONS)")
        parser.add_argument("url", type=str, help="URL для запроса (например, http://127.0.0.1:8080/file.txt)")
        parser.add_argument("-d", "--data", type=str, help="Тело запроса (POST)")
        parser.add_argument("-H", "--headers", nargs="+", help="Дополнительные заголовки (например, key:value)")
        self.args =  parser.parse_args()

    def send_request(self):
        try:
            while True:
                ##Перенести это дело в класс запроса
                host, path = self.args.url.split('//')[1].split('/', 1)
                request = f"{self.args.method} {path} HTTP/1.1\r\nHost: {host}\r\n"
                if self.args.headers:
                    for header in self.args.headers:
                        key, value = header.split(":")
                        request += f"{key}: {value}\r\n"
                if self.args.data:
                    request += f"Content-Length: {len(self.args.data)}\r\n"
                    request += "\r\n" + self.args.data
                else:
                    request += "\r\n"
                self.client.sendall(request.encode())
                self.get_response(self.args.method)
        finally:    
            self.client.close()

    def get_response(self, method: str):
        response = self.client.recv(4096).decode()
        if method == "GET":
            ##  ВОТ ТУТ НАДО ПАРСИТЬ ОТВЕТ ЖЕЛАТЕЛЬНО В КЛАССЕ ОТВЕТА. ПОДУМАТЬ
            pass
        else:
            print(response)

    def GET_handler(self):
        pass

if __name__ == '__main__':
    client = Client('localhost', 3030)
    client.send_request()