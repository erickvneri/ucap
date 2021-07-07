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
import usocket as socket
import machine

import public as views

class Request:
    # Request class to provide
    # clean interface to incoming
    # HTTP requests.
    #   ::param status: str
    #       First line
    #       of the HTTP Request
    #   ::param headers: dict
    #       Headers of incoming
    #       HTTP Request
    def __init__(self, status: str, headers: dict):
        self.status = status
        self.headers = headers

class Server:
    # HTTP Server on top of the
    # <socket> module that opens
    # at the default 192.168.4.1
    # address according to the
    # Access Point IP and listens
    # at the port 80 by default.
    #
    # It has been designed to provide
    # a local control interface.
    def __init__(self, addr='', port=80):
        self.addr = addr
        self.port = port
        self.limit = 1
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.bind((self.addr, self.port))
        except OSError as e:
            print('socket error', e)
            machine.reset()

    @staticmethod
    def parsehttp(payload):
        # HTTP Request parser that
        # takes the string payload
        # and returns a Request
        # object for ease of use of
        # HTTP requests.
        lines = payload.splitlines()

        headers = {}
        for i in range( len(lines[1:])-1 ):
            h = lines[i+1].split(': ')
            headers[h[0].lower()] = h[1]

        status = lines[0]
        return Request(status, headers)

    @staticmethod
    def route(conn, req):
        # Route requests based on
        # the supported device
        # resources.
        print(req.status)
        if '/about' in req.status:
            print('FIXME: HANDLE /about')
        elif '/control' in req.status:
            print('FIXME: HANDLE /control')
        elif '/setup' in req.status:
            print('FIXME: HANDLE /setup')
        elif '/favicon.ico' in req.status:
            conn.send(views.index)
        conn.send(views.index)
        conn.close()

    async def listen(self):
        # Coroutine that will
        # listen incoming requests.
        self.sock.listen(self.limit)

        while True:
            # Catch incomming request
            # and address of client
            conn, addr = self.sock.accept()
            # Parse the HTTP Request into
            # a Request object separating
            # the status (first line) to
            # ease routing
            req = self.parsehttp(
                conn.recv(1024).decode('utf-8'))
            self.route(conn, req)
