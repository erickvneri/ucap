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
import gc
import ujson as json


class Request:
    # Request interface to provide
    # a clean-as-possible interface
    # to handle HTTP Requests.
    # ::param body: string, identified
    #   by a full new line between
    #   the headers.
    # ::param headers: dict
    # ::param method: str
    # ::param path: str
    # ::param protocol: str, often HTTP
    #   version
    def __init__(
        self,
        body: str,
        headers: dict,
        method: str,
        path: str,
        protocol: str,
        route: str,
    ) -> "Request":
        self.body = body
        self.headers = headers or {}
        self.method = method
        self.path = path
        self.protocol = protocol
        self.route = route

        # RELEASE args REFERENCE
        body = None
        headers = None
        method = None
        path = None
        protocol = None
        route = None
        # RUN GARBAGE COLLECTOR
        gc.collect()

    def get_json(self) -> dict:
        # Returns a dictionary from
        # a JSON string
        try:
            res = json.loads(self.body)
        except ValueError as e:
            print("Warning: not a valid JSON payload to decode,", e)
        else:
            return res

    @classmethod
    def from_string(cls, payload: str) -> "Request":
        # Parse HTTP Request from raw
        # payload and returns a Request
        # object.
        _colon_sep = ": "
        _qs_sep = "?"
        _lnsep = "\r\n\r\n"

        # unpack request and body
        req = tuple(payload.split(_lnsep))

        # RELEASE "payload" REFERENCE
        payload = None

        if len(req) > 1:
            req, body = req
        else:
            req = req[0]
            body = None

        # split request string
        lns = req.splitlines()

        # RELEASE "req" REFERENCE
        req = None

        # unpack request status
        method, path, protocol = tuple(lns[0].split())
        route = path if path.find(_qs_sep) < 1 else path[: path.find(_qs_sep)]

        # unpack headers
        headers = {}
        for h in lns[1:]:
            h = h.split(_colon_sep)
            if len(h) > 1:
                headers[h[0]] = h[1]

        # RUN GARBAGE COLLECTOR
        gc.collect()

        # return Request instance
        return cls(body, headers, method, path, protocol, route)
