# Copyright 2021 bardovasco
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import uasyncio as asyncio
from request import Request


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

    async def _invoke_handler(self, res, handler, payload):
        # Resource that invokes the
        # route/endpoint handler registered
        # by the uCap.route decorator.
        handler_response = handler(payload)
        await res.awrite(handler_response)
        await res.wait_closed()

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
            # monkey patch for
            # future default Error
            # response.
            error_res = \
                ('HTTP/1.1 404 Not Found\n'+\
                'Content-Type: text/plain\n\n'+\
                'Resource Not Found')
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

    def run(self, addr='0.0.0.0', port=80):
        # This resourse return the
        # Server class whose handler
        # will be scheduled by the
        # asyncio loop.
        return asyncio.start_server(
            self._listen, addr, port)

