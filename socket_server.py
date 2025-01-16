import socket
import logging
import os
import mimetypes
from message import HTTP_Request, HTTP_Response

class Server:
    def __init__(self, directory, host, port):
        self.directory = directory
        
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.__host = host
        self.__port = port
        self.sock = socket.socket() 
        self.sock.bind((self.__host, self.__port))
        self.sock.listen(5)
        
        self.file_log = logging.FileHandler('log', encoding='utf-8')
        self.console_log = logging.StreamHandler()
        logging.basicConfig(handlers=(self.file_log, self.console_log), level=logging.INFO)
        logging.info("Инициализация сервера")


    def handle_request(self, request) -> HTTP_Response:
        try:
            logging.info("Обработка запроса")
            req = HTTP_Request(request)
            if req.method == "GET":
                return self.GET_handler(req)
            elif req.method == "POST":
                return self.POST_handler(req)
            elif req.method == "OPTIONS":
                logging.info()
                return self.OPTIONS_handler(req)
            else:
                return self.not_allowed_handler(req)
        except:
            logging.error("Ошибка обработки запроса")
            return HTTP_Response(code=500, body=req.body)
    
    def GET_handler(self, req: HTTP_Request) -> HTTP_Response:
        try:
            logging.info("Get запрос")
            if req.uri.startswith("/"):
                req.uri = req.uri.lstrip("/")
            with open(req.uri, "rb") as file:
                body = file.read()
            mime_type, _ = mimetypes.guess_type(req.uri)
            if not mime_type: 
                mime_type = "application/octet-stream"
            headers = {
                "Content-Disposition": req.uri,
                "Content-Type": mime_type,
                "Content-Length": str(len(body))
            }
            return HTTP_Response(code=200, body=body, headers=headers)
        except Exception as a:
            return HTTP_Response(code=404, body=b"File not found")

    def POST_handler(self, req: HTTP_Request) -> HTTP_Response:
        logging.info("POST запрос")
        return HTTP_Response(code=200, body=req.body)

    def OPTIONS_handler(self, req: HTTP_Request) -> HTTP_Response:
        logging.info("OPTIONS запрос")
        headers = {"Allow": "GET, POST, OPTIONS"}
        return HTTP_Response(code=200, headers=headers)

    def not_allowed_handler(self, req: HTTP_Request) -> HTTP_Response:
        logging.info("Not Allowed")
        return HTTP_Response(code=405, body=b"Method Not Allowed")

    def start_server(self):
        try:
            while True:
                client_sock, client_addr = self.sock.accept()
                with client_sock:
                    logging.info(f"Подключение клиента {client_addr}")
                    request = client_sock.recv(1024).decode()
                    response = self.handle_request(request)
                    client_sock.sendall(response.make_response())
                    
        except OSError as e:
            logging.error(f"Ошибка сокета: {e}")
        finally:
            self.sock.close()
            logging.info("Сервер остановлен")

if __name__ == '__main__':
    server = Server('files', 'localhost', 3030)
    server.start_server()