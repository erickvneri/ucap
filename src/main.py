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

import server

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

async def ap_init(event_handler):
    # Built-in access point service
    # to provide futher network config
    # and device control and monitoring
    # interface.
    #
    # In addition, as the access point
    # is part of the core app features
    # it has been included and started
    # up at main.py as a coroutine.
    try:
        ap = network.WLAN(network.AP_IF)
        ap.config(essid=_ap_env['essid'])
        ap.config(password=_ap_env['key'])
        ap.config(max_clients=_ap_env['max_conn'])
        ap.config(hidden=_ap_env['hidden'])
        ap.config(authmode=_ap_env['authmode'])
    except:
        machine.soft_reset()
    else:
        ap.active(1)

        noti = 0  # event notification flag
        while 1:
            # Actual coroutine loop that
            # will monitor connections
            # into the access point and
            # emit such events.
            await asyncio.sleep_ms(1000)
            conn, stas = ap.isconnected(), ap.status('stations')

            if conn and not noti:
                # new connection that
                # hasn't beennot notified.
                event_handler((conn, stas))
                noti = 1
            elif not conn and noti:
                # station disconnected that
                # was previously notified
                # when established connection.
                event_handler((conn, stas))
                noti = 0

def main():
    srv = server.Server()

    loop = asyncio.get_event_loop()
    loop.create_task(ap_init(lambda s: print(s))) # mock event handler
    loop.create_task(srv.listen())
    loop.run_forever()

if __name__ == '__main__':
    main()
