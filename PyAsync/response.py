try:
    import ujson as json
except ImportError:
    import json

import http.server

web_responses = http.server.BaseHTTPRequestHandler.responses


class Response:
    def __init__(
            self,
            body=None,
            status=200,
            content_type="application/json",
            headers=None,
            version="1.1",
    ):
        self._version = version
        self._status = status
        self._encoding = "utf-8"
        self._body = body
        self._content_type = content_type
        if headers is None:
            headers = {}
        self._headers = headers

    @property
    def body(self):
        return self._body

    @property
    def status(self):
        return self._status

    @property
    def content_type(self):
        return self._content_type

    @property
    def headers(self):
        return self._headers

    def add_body(self, data):
        self._body = data

    def add_header(self, key, value):
        self._headers[key] = value

    def __str__(self):
        status_msg, _ = web_responses.get(self._status)
        messages = [
            f"HTTP/{self._version} {self._status} {status_msg}",
            f"Content-Type: {self._content_type}",
            f"Content-Length: {len(self._body)}",
            f"Connection: close"
        ]

        if self._headers:
            for header, value in self._headers.items():
                messages.append(f"{header}: {value}")

        if self._body is not None:
            messages.append("\n" + self._body)

        return "\n".join(messages)

    def __repr__(self):
        return f"<Response status={self._status} content_type={self._content_type}>"


def make_success_response(data: dict, status_code: int = 200, meta: dict = {}) -> Response:
    """
    Function to make Success Json Response
    :params data {}
    :params status_code
    :params meta {}
    """
    response = {
        'data': data,
        'meta': meta,
        'is_success': True,
        'status_code': status_code
    }
    return Response(status=status_code, body=json.dumps(response), content_type="application/json")


def make_error_response(error: str, status_code: int) -> Response:
    """
    Function to make Success Json Response
    :params error
    :params status_code
    :params status_code
    """
    error = {
        "error": [{"message": error}],
        "is_success": False,
        "status_code": status_code,
    }
    return Response(status=status_code, body=json.dumps(error), content_type="application/json")
