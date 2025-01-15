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