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
import machine
import network
import uasyncio as asyncio

from app import create_app

# For the improvement on
# the security of these
# values, this must be encrypted
# and decrypted while reading it.
_ap_env = dict(
    essid="ESP32-demo",
    key="dummy-passphrase",
    max_conn=1,
    hidden=0,
    authmode=network.AUTH_WPA_WPA2_PSK,
)


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
    ap.config(essid=_ap_env["essid"])
    ap.config(password=_ap_env["key"])
    ap.config(max_clients=_ap_env["max_conn"])
    ap.config(hidden=_ap_env["hidden"])
    ap.config(authmode=_ap_env["authmode"])
    ap.active(1)


def main():
    wifiap_init()
    app = create_app()

    # Initialize event loop
    loop = asyncio.get_event_loop()

    # Schedule tasks
    loop.create_task(app.run())

    # initialize loop
    loop.run_forever()


if __name__ == "__main__":
    main()
