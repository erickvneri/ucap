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
from ucap import uCap
from ucap.helpers import from_stylesheet, from_html


def create_app():
    app = uCap()

    # FIXME: Monkey application route
    @app.route("/styles.css")
    def styles(req):
        return from_stylesheet("templates/styles.css")
        # return templates["styles"], 200

    # FIXME: Monkey application route
    @app.route("/about")
    def about(req):
        return from_html("templates/about.html")
        # return templates["about"], 200

    # FIXME: Monkey application route
    @app.route("/wifi-setup")
    def about(req):
        return from_html("templates/wifi-setup.html")

    # FIXME: Monkey application route
    @app.route("/wifi-connect")
    def wifi_connect(req):
        return from_html("templates/wifi-setup.html")

    # FIXME: Monkey application route
    # @app.route("/control")
    # def metadata(req):
    # return templates["device-control"], 200

    return app
