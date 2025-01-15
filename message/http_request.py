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