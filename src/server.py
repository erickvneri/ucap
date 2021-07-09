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
from ucap.request import Request


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
            req = conn.recv(1024).decode('utf-8')
            request = Request.from_string(req)
            print(request.__dict__)
            conn.send(views.index)
