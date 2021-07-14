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
import ujson as json


class StatusEnum:
    # Status code enum that
    # supports for the most
    # common and used codes
    # for XMLHR
    OK = "200 OK"
    CREATED = "201 Created"
    NOT_FOUND = "404 Not Found"
    UNAUTHORIZED = "401 Unauthorized"
    SERVER_ERROR = "500 Internal Server Error"


class ContentTypeEnum:
    # Content type enum supporting
    # the most common and used
    # content types for XMLHR
    HTML = "text/html"
    TEXT = "text/plain"
    XML = "application/xml"
    JSON = "application/json"


class Response:
    # Response constructor to build
    # HTTP Responses from a status
    # code enumerator (StatusEnum)
    # and the payload as a list of
    # string lines of the template
    # Use example:
    # res = Response(
    # StatusEnum.OK
    # {'hello': 'world'})
    # print(res.lines)
    # [
    # 'HTTP/1.1 200 OK\nContent-Type: application/json\nContent-Lenght: 18',
    # '\n\n',
    # '{"hello": "world"}'
    # ]
    def __init__(self, status: StatusEnum, payload: list):
        self.status = "HTTP/1.1 *".replace("*", status)
        self.headers = None
        self.content_type = None
        self.content_length = None
        self.lines = None
        # Validate type and integrity
        # of payload.
        # Warning:
        # This isn't an exaustive check,
        # hence, try passing a proper
        # payload data as argument
        self.payload = self.validate_payload(payload)
        self.build()

    def build(self):
        self.content_type = self.set_content_type(self.payload[0])
        self.content_length = self.set_content_lenght(self.payload)
        self.headers = "\n".join(
            [
                self.status,
                "Content-Type: *".replace("*", self.content_type),
                "Content-Lenght: *".replace("*", str(self.content_length)),
            ]
        )
        self.lines = [self.headers] + ["\n\n"] + self.payload

    @staticmethod
    def validate_payload(payload):
        if type(payload) is dict:
            return [json.dumps(payload)]
        elif type(payload) is str:
            return [payload]
        elif type(payload) is list:
            return payload
        else:
            raise TypeError(
                "Received payload:%s, expected [dict, str, list]" % type(payload)
            )

    @staticmethod
    def set_content_type(fline):
        if "html" in fline:
            return ContentTypeEnum.HTML
        elif "xml" in fline:
            return ContentTypeEnum.XML
        elif "{" == fline[0]:
            return ContentTypeEnum.JSON
        return ContentTypeEnum.TEXT

    @staticmethod
    def set_content_lenght(payload):
        return len("".join(payload))
