# uCap

### Description

Embedded microframework written in MicroPython that facilitates
the development of device web interfaces or backend services through
readable and shorthand endpoint declarations.

It has been built on top of the MicroPython `uasyncio` module, hence
the server enabled is a coroutine that must be assigned as a task or
gathered by the `uasyncio` event loop.

### Usage example:

- `uCap` app instance and route definition:

```python
from ucap import uCap
from ucap.helpers import send_stylesheet, send_html, send_xml


def create_app():
    app = uCap()

    # Fetch stylesheet referenced about
    # HTML <link> metadata tag
    @app.route("/styles.css")
    def styles(req):
        return send_stylesheet("templates_directory/styles.css")

    # Send a raw <h1> HTML tag
    @app.route("/hello-world")
    def hello_world(req):
        return send_html(raw_input="<h1>Hello world!</h1>")

    # Mock wifi setup
    # authenticator page
    @app.route("/wifi-setup")
    def about(req):
        return send_html("templates_directory/wifi-setup.html")

    # wifi authenticator handler
    # which will only print
    # the JSON payload received
    @app.route("/wifi-connect")
    def wifi_connect(req):
        print(req.get_json())
        return send_html("templates_directory/wifi-setup.html")

    return app
```
