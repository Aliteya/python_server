import socket
import logging
import os

class HTTP_Response():
    def __init__(self, code: int, reason: str = None, body: bytes = None):
        self.code = code
        self.reason = reason or self._get_default_reason(code)
        self.body = body
        #ПОДУМАТЬ КАК ПЕРЕДАВАТЬ ТИП КОНТЕНТА

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


    def handle_request(self, request):
        # try:
        ##ПОДУМАТЬ КАК УНИВЕРСАЛЬНО ДОСТАВАТЬ ДАННЫЕ
            request = request.split()
        
            # method, host, path 
            return "testkjfdl"
        # except:
        #     logging.error("Ошибка обработки запроса")
        #     return "errtest"
    
    def GET_handler(self):
        pass

    def POST_handler(self):
        pass

    def OPTIONS_handler(self):
        pass

    def start_server(self):
        try:
            while True:
                client_sock, client_addr = self.sock.accept()
                with client_sock:
                    logging.info(f"Подключение клиента {client_addr}")
                    request = client_sock.recv(1024).decode()
                    response = self.handle_request(request)
                    client_sock.sendall(response.encode())
                    
        except OSError as e:
            logging.error(f"Ошибка сокета: {e}")
        finally:
            self.sock.close()
            logging.info("Сервер остановлен")

if __name__ == '__main__':
    server = Server('files', 'localhost', 3030)
    server.start_server()