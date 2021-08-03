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
from ucap.response import Response, ContentTypeEnum


def _read_path_lines(path) -> list:
    # Return an array of file
    # line of the specified path
    content = None
    try:
        _f = open(path)
    except OSError as e:
        print("Invalid path", e)
    else:
        content = _f.readlines()
    finally:
        _f.close()
        return content


def send_stylesheet(path=None, *, raw_input=None):
    # Lazyload an HTML template
    # file and returns a Response
    # object
    if path:
        content = _read_path_lines(path)
    elif style:
        content = raw_input.split("\n")
    return Response(200, content, ContentTypeEnum.CSS)


def send_html(path=None, *, raw_input=None):
    # Lazyload an HTML template
    # file and returns a Response
    # object
    if path:
        content = _read_path_lines(path)
    elif raw_input:
        content = raw_input.split("\n")
    return Response(200, content, ContentTypeEnum.HTML)


def send_xml(path=None, *, raw_input=None):
    # Lazyload an XML template
    # file and returns a Response
    # object
    if path:
        content = _read_path_lines(path)
    elif raw_input:
        content = raw_input.split("\n")
    return Response(200, content, ContentTypeEnum.XML)
