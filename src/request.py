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
        self, body: str,
              headers: dict,
              method: str,
              path: str,
              protocol: str,
              route: str) -> 'Request':
        self.body = body
        self.headers = headers or {}
        self.method = method
        self.path = path
        self.protocol = protocol
        self.route = route


    @classmethod
    def from_string(cls, payload: [bytes, str]) -> 'Request':
        """
        Parse HTTP Request from raw payload and
        returns a Request object.
        """
        _colon_sep = b': ' if type(payload) is bytes else ': '
        _qs_sep = b'?' if type(payload) is bytes else '?'
        _lnsep = b'\n\n' if type(payload) is bytes else '\n\n'

        # unpack request and body
        req = tuple(payload.split(_lnsep))
        if len(req) > 1: req, body = req
        else: req = req[0]; body = None

        # split request string
        lns = req.splitlines()

        # unpack request status
        method, path, protocol = tuple(lns[0].split())
        route = path if path.find(_qs_sep) < 1 else path[:path.find(_qs_sep)]

        # unpack headers
        headers = {}
        for h in lns[1:]:
            h = h.split(_colon_sep)
            if len(h) > 1:
                headers[h[0]] = h[1]

        # return Request instance
        return cls(
            body,
            headers,
            method,
            path,
            protocol,
            route)

