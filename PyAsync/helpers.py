"""
Helper functions
"""

import traceback
from urllib.parse import urlsplit, parse_qs
from .response import make_error_response
from .exceptions import HTTPException
from .response import Response

server_exception = """
500 Internal server error. Server got itself in trouble : {exc} {traceback}
"""


def format_exception(exc: HTTPException) -> Response:
    """
    :params Exception
    """
    trace = traceback.format_exc().replace("\n", "</br>")
    msg = server_exception.format(exc=str(exc), traceback=trace)
    return make_error_response(error=msg, status_code=500)


def get_query_params(url: str) -> dict:
    """
    Function to get query parameters from URL
    :params url
    :return {'key': value}
    """
    _query_params = {}
    try:
        url = "http://www.google.com" + str(url)
        query = urlsplit(url).query
        params = parse_qs(query)
        _query_params = {k: v[0] for k, v in params.items()}
    except Exception as e:
        print(str(e))
        _query_params = {}
    return _query_params
