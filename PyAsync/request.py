import json

from yarl import URL


class Request:
    #
    def __init__(self, method, url, headers, version=None, body=None, app=None):
        self._version = version
        self._encoding = "utf-8"
        self._method = method.decode(self._encoding)
        self._url = URL(url.decode(self._encoding))
        self._headers = headers
        self._body = body
        self._app = app
        self._match_info = {}
        self._query_params = {}
        self._raw_url = url

    @property
    def app(self):
        return self._app

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, query_params):
        url = self._url
        dict = {}
        try:
            split_url = url.split("?")[1]
            dict = {x[0]: x[1] for x in [x.split("=") for x in split_url[1:].split("&")]}
        except Exception as e:
            self._query_params = dict
        self._query_params = dict

    @property
    def match_info(self):
        return self._match_info

    @match_info.setter
    def match_info(self, match_info):
        self._match_info = match_info

    @property
    def method(self):
        return self._method

    @property
    def url(self):
        return self._url

    @property
    def headers(self):
        return self._headers

    def text(self):
        if self._body is not None:
            return self._body.decode(self._encoding)

    async def json(self):
        text = self.text()
        if text is not None:
            return json.loads(text)

    def __repr__(self):
        return f"<Request at 0x{id(self)}>"
