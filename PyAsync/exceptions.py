"""
HTTPException is responsible for handling all HTTP Exceptions.
"""


from .response import Response


class HTTPException(Response, Exception):
    status_code = None

    def __init__(self, reason=None, content_type=None):
        self._reason = reason
        self._content_type = content_type

    @property
    def reason(self):
        return self._reason


class HTTPNotFound(HTTPException):
    status_code = 404


class HTTPBadRequest(HTTPException):
    status_code = 400


class HTTPUnAuthorized(HTTPException):
    status_code = 401


class HTTPForbidden(HTTPException):
    status_code = 403


class HTTPInternalServerError(HTTPException):
    status_code = 500


class HTTPUnProcessableEntityError(HTTPException):
    status_code = 422


class HTTPMethodNotAllowed(HTTPException):
    status_code = 405


class HTTPFound(HTTPException):
    status_code = 302

    def __init__(self, location, reason=None, content_type=None):
        super().__init__(reason=reason, content_type=content_type)
        self.add_header("Location", location)

