import socket
import logging
import os
import mimetypes

class HTTP_Request:
    def __init__(self, raw_request: str):
        self.method = None
        self.uri = None
        self.http_version = None
        self.headers = {}
        self.body = None
        self._parse_request(raw_request)

    def _parse_request(self, raw_request: str):
        lines = raw_request.split("\r\n")
        if len(lines) < 1:
            raise ValueError("Invalid HTTP request format")

        request_line = lines[0].split(" ")
        if len(request_line) != 3:
            raise ValueError(f"Invalid request line: {lines[0]}")
        self.method, self.uri, self.http_version = request_line
  
        headers = {}
        i = 1
        while i < len(lines) and lines[i] != "":
            header_parts = lines[i].split(": ", 1)
            if len(header_parts) == 2:
                headers[header_parts[0]] = header_parts[1]
            i += 1
        self.headers = headers

        body_start = i + 1
        if body_start < len(lines):
            self.body = "\r\n".join(lines[body_start:]).strip()
        else:
            self.body = ""

    def get_header(self, header_name: str) -> str:
        return self.headers.get(header_name)

    def __str__(self):
        return (
            f"HttpRequest(method={self.method}, uri={self.uri}, "
            f"http_version={self.http_version}, headers={self.headers}, body={self.body})"
        )


class HTTP_Response():
    def __init__(self, code: int, reason: str = "", body: bytes = b"", headers: dict = {}):
        self.code = code
        self.reason = reason or self._get_default_reason(code)
        self.body = body
        self.headers = headers
    
    def add_header(self, key: str, value: str):
        self.headers[key] = value
    
    def make_response(self):
        response = f"HTTP/1.1 {self.code} {self.reason}\r\n"
        headers_lines = [f"{key}:{value}\r\n" for key, value in self.headers.items()]
        response += ''.join(headers_lines)
        response += "\r\n"
        response = response.encode() + self.body
        return response

    @staticmethod
    def _get_default_reason(code: int) -> str:
        reasons = {
            200: "OK",
            404: "Not found",
            405: "Method not allowed",
            505: "Internal server error",
        }
        return reasons.get(code, "Не прописан такой статус код")

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
            req = HTTP_Request(request)
            print(req.headers, req.method)
        ##ПОДУМАТЬ КАК УНИВЕРСАЛЬНО ДОСТАВАТЬ ДАННЫE
            if req.method == "GET":
                return self.GET_handler(req)
            elif req.method == "POST":
                return self.POST_handler(req)
            elif req.method == "OPTIONS":
                return self.OPTIONS_handler(req)
            else:
                return self.not_allowed_handler(req)
        except:
            logging.error("Ошибка обработки запроса")
            return HTTP_Response(code=500, body=req.body)
    
    def GET_handler(self, req: HTTP_Request) -> HTTP_Response:
        try:
            if req.uri.startswith("/"):
                req.uri = req.uri.lstrip("/")
            with open(req.uri, "rb") as file:
                body = file.read()
            mime_type, _ = mimetypes.guess_type(req.uri)
            if not mime_type: 
                mime_type = "application/octet-stream"
            headers = {
                "Content-Type": mime_type,
                "Content-Length": str(len(body))
            }
            return HTTP_Response(code=200, body=body, headers=headers)
        except Exception as a:
            print(a)
            return HTTP_Response(code=404, body=b"File not found")

    def POST_handler(self, req: HTTP_Request) -> HTTP_Response:
        return HTTP_Response(code=200, body=req.body)

    def OPTIONS_handler(self, req: HTTP_Request) -> HTTP_Response:
        try:
            headers = {"Allow": "GET, POST, OPTIONS"}
            return HTTP_Response(code=200, body=req.body, headers=headers)
        except:
            return HTTP_Response(code=404, body=req.body, headers=req.headers)

    def not_allowed_handler(self, req: HTTP_Request) -> HTTP_Response:
        return HTTP_Response(code=405, body=req.body, headers=req.headers)

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