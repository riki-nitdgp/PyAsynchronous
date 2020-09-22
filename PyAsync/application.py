import asyncio
import signal
from functools import  wraps, partial

from .exceptions import HTTPException
from .helpers import format_exception
from .response import Response
from .router import UrlDispatcher
from .server import Server as srv


class Application:
    def __init__(self, loop=None, middlewares=None):
        if loop is None:
            loop = asyncio.get_event_loop()

        self._loop = loop
        self._router = UrlDispatcher()
        self._on_startup = []
        self._on_shutdown = []

        if middlewares is None:
            middlewares = []
        self._middlewares = middlewares

    @property
    def loop(self):
        return self._loop

    @property
    def router(self):
        return self._router

    @property
    def on_startup(self):
        return self._on_startup

    @property
    def on_shutdown(self):
        return self._on_shutdown

    def route(self, path, method="GET"):
        """
        Decorator Function for handler registration
        :params path
        :params method
        """

        @wraps(func)
        def handle(func):
            self._router.add_route(method, path, func)

        return handle

    async def startup(self):
        coros = [func(self) for func in self._on_startup]
        await asyncio.gather(*coros, loop=self._loop)

    async def shutdown(self):
        print("Shutdown process")
        coros = [func(self) for func in self._on_shutdown]
        await asyncio.gather(*coros, loop=self._loop)

    def _make_server(self):
        return srv(loop=self._loop, handler=self._handler, app=self)

    async def _handler(self, request, response_writer):
        """
        Process incoming request
        :params request -> Request
        :params response_writer
        """
        try:
            match_info, handler = self._router.resolve(request)

            request.match_info = match_info

            if self._middlewares:
                for md in self._middlewares:
                    handler = partial(md, handler=handler)

            resp = await handler(request)
        except HTTPException as exc:
            resp = exc
        except Exception as exc:
            resp = format_exception(exc)

        if not isinstance(resp, Response):
            raise RuntimeError(f"expect Response instance but got {type(resp)}")

        response_writer(resp)


def run_app(app, host="127.0.0.1", port=8080, loop=None):
    """
    Function to run the application
    :params app ->Application
    :params host
    :params port
    :params loop
    """
    if loop is None:
        loop = asyncio.get_event_loop()

    protocol = app._make_server()
    loop.run_until_complete(app.startup())

    server = loop.run_until_complete(
        loop.create_server(lambda: protocol, host=host, port=port)
    )

    loop.add_signal_handler(
        signal.SIGTERM, lambda: asyncio.ensure_future(app.shutdown())
    )

    try:
        print(f"Started server on {host}:{port}")
        loop.run_until_complete(server.serve_forever())
    except KeyboardInterrupt:
        # TODO: Graceful shutdown here
        loop.run_until_complete(app.shutdown())
        server.close()
        loop.stop()
