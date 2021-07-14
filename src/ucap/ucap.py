# MIT License
#
# Copyright (c) 2021 bardovasco
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import uasyncio as asyncio

# local modules
from ucap.request import Request


class uCap:
    def __init__(self):
        self.routes = {}

    def route(self, route):
        # Route decorator to assign
        # a specific resource handler.
        # It will be stored at the
        # self.routes dict for future
        # use.
        # Use example:
        #   @app.route('/route')
        #   def handler(req):
        #       pass
        def decorator(handler):
            self.routes[route.encode()] = handler

        return decorator

    @staticmethod
    async def _send(res, buff):
        # FIXME: Implement Response.ok_200(buff)
        # which will handle join of HTTP Status
        # and headers.
        _status = [
            res.write(l)
            for l in [
                "HTTP/1.1 200 OK\n",
                "Content-Type: text/html\n",
                "Content-Lenght: " + str(len("".join(buff))),
                "\n\n",
            ]
        ]
        if type(buff) is list:
            [res.write(ln) for ln in buff]
        else:
            # FIXME: Handle json respones
            # for third party integrations
            # supporting JSON over HTTP.
            pass
        await res.drain()
        await res.wait_closed()

    async def _invoke_handler(self, res, handler, payload):
        # Resource that invokes the
        # route/endpoint handler registered
        # by the uCap.route decorator.
        handler_response = handler(payload)
        return await self._send(res, handler_response)

    async def _validate_route(self, res, route, payload):
        # Route validator that check
        # if the route/endopoint called
        # has been registered using the
        # uCap.route resource. Example:
        #   @app.route('/route'):
        #   def handler(request):
        #       pass
        handler = self.routes.get(route)
        if not handler:
            # FIXME: Implement Response.not_found()
            # monkey patch for
            # future default Error
            # response.
            error_res = (
                "HTTP/1.1 404 Not Found\n"
                + "Content-Type: text/plain\n\n"
                + "Resource Not Found"
            )
            await res.awrite(error_res)
            await res.wait_closed()
        else:
            await self._invoke_handler(res, handler, payload)

    async def _listen(self, req, res):
        # Server handler coroutine
        # that receives the req and
        # res (reader, writer) streams
        # and parse and pass the Request
        # object into the route validator.
        req = await req.read(1024)
        request = Request.from_string(req)
        await self._validate_route(res, request.route, request)

    def run(self, addr="0.0.0.0", port=80):
        # This resourse return the
        # Server class whose handler
        # will be scheduled by the
        # asyncio loop.
        return asyncio.start_server(self._listen, addr, port)