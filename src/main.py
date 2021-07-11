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
import machine
import network
import uasyncio as asyncio

from ucap import uCap
from request import Request
# For the improvement on
# the security of these
# values, this must be encrypted
# and decrypted while reading it.
_ap_env = dict(
    essid='ESP32-demo',
    key='dummy-passphrase',
    max_conn=1,
    hidden=0,
    authmode=network.AUTH_WPA_WPA2_PSK)

def wifiap_init():
    # Built-in access point service
    # to provide futher network config
    # and device control and monitoring
    # interface.
    #
    # In addition, as the access point
    # is part of the core app features
    # it has been included and started
    # up at main.py as a coroutine.
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=_ap_env['essid'])
    ap.config(password=_ap_env['key'])
    ap.config(max_clients=_ap_env['max_conn'])
    ap.config(hidden=_ap_env['hidden'])
    ap.config(authmode=_ap_env['authmode'])
    ap.active(1)
    ap.active(1)

async def loop_1():
    while True:
        await asyncio.sleep_ms(1000)
        print('Loop 1')

async def loop_2():
    while True:
        await asyncio.sleep_ms(1000)
        print('Loop 2')

def main():
    wifiap_init()
    app = uCap()

    # App routes
    @app.route('/index')
    def index(req):
        print(req.__dict__)
        return ('HTTP/1.1 200 OK\n'+\
                'Content-Type: text/plain\nContent-Lenght: 15'+\
                '\n\nHello world!')

    # Initialize event loop
    loop = asyncio.get_event_loop()

    # server coro
    loop.create_task(app.run())

    # initialize loop
    loop.run_forever()


if __name__ == '__main__':
    main()

