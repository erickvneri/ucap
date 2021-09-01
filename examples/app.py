# MIT License
#
# Copyright (c) 2021 erickvneri
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
from ucap.helpers import send_stylesheet, send_html, send_xml


def create_app():
    app = uCap()

    # Example route that returns
    # stylesheet template that has
    # been referenced on <link> HTML
    # tag.
    @app.route("/styles.css")
    def styles(req):
        return send_stylesheet("mock_templates/styles.css")

    @app.route("/wifi-setup")
    def about(req):
        return send_html("mock_templates/wifi-setup.html")

    @app.route("/wifi-connect")
    def wifi_connect(req):
        print(req.get_json())
        return send_html("mock_templates/wifi-setup.html")

    @app.route("/control")
    def control(req):
        return send_html("mock_templates/device-control.html")

    @app.route("/xml")
    def xml(req):
        return send_xml("mock_templates/xml_example.xml")

    @app.route("/hello-world")
    def hello_world(req):
        return send_html(raw_input="<h1>Hello world!</h1>")

    return app
