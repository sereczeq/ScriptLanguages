import re


class BadRequestError(Exception):
    pass


class BadHTTPVersion(Exception):
    pass


class WrongArgumentCount(Exception):
    pass


class Request:
    def __init__(self, request: str):
        if type(request) is not str:
            raise TypeError("Object must be type string")

        arguments = request.split()

        if len(arguments) != 3:
            raise WrongArgumentCount

        # Now I know how to make it work ^^
        self.type, self.path, self.protocol = arguments
        # self.type = arguments[0]
        # self.path = arguments[1]
        # self.protocol = arguments[2]

        # quickly copied from other lab
        if self.type not in "GET|POST|HEAD|PUT|DELETE|TRACE|OPTIONS|CONNECT|PATCH":
            raise BadRequestError

        for version in ["1.0", "1.1", "2.0"]:
            if version in self.protocol:
                break
        else:
            raise BadHTTPVersion

        if self.path[0] != "/":
            raise ValueError('“Path must start with /” if the path does not start with the slash (“/”) character')

    # def __init__(self, request: str):
    #     if type(request) is not str:
    #         raise TypeError("Object must be type string")
    #     array = request.split()
    #     self.type = array[0]
    #     self.path = array[1]
    #     self.protocol = array[2]

    # def __init__(self, request: str):
    #
    #     if type(request) is not str:
    #         raise TypeError("Object must be type string")
    #
    #     regex = "(?P<ipAddress>(\\d{1,3}\\.){3}\\d{1,3}) - - " \
    #             "(?P<timeStamp>\\[\\d{1,2}\\/[A-Z][a-z]{2}\\/\\d{4}(:\\d{2}){3} \\+\\d{4}]) " \
    #             "(?P<requestHeader>\"(?P<type>[A-Z]+?) (?P<resource>\\/[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*?)" \
    #             " (?P<protocol>[A-Z]+?\\/[\\d.]+))\" " \
    #             "(?P<httpStatusCode>\\d{3}) " \
    #             "(?P<sizeOfResponse>\\d+?) "
    #     match = re.match(regex, request)
    #
    #     if match:
    #         self.type = match.group("type")
    #         self.path = match.group("resource")
    #         self.protocol = match.group("protocol")
    #     else:
    #         raise Exception("Invalid log line")

    def __repr__(self):
        return f'Request{{type: {self.type}, path: {self.path}, protocol: {self.protocol}}}'


# changed the name accordingly to PEP
def request_string_to_object(request_string):
    try:
        return Request(request_string)
    except WrongArgumentCount:
        return None


import pytest


# 1
def test_request_string_to_object_check_argument_type():
    with pytest.raises(TypeError):
        request_string_to_object(123)


# 2
def test_request_init_check_return_type():
    assert type(request_string_to_object("GET / HTTP1.1")) is Request


# 3
def test_request_init_check_variables():
    request = request_string_to_object("GET / HTTP1.1")
    assert request.type == "GET"
    assert request.path == "/"
    assert request.protocol == "HTTP1.1"


# 4
def test_request_init_check_variables_more():
    type = "POST"
    path = "/stupid.cat"
    protocol = "HTTP1.0"
    string = type + " " + path + " " + protocol
    request = request_string_to_object(string)
    assert request.type == type
    assert request.path == path
    assert request.protocol == protocol


# 5
def test_request_init_only_two_args():
    assert type(request_string_to_object("GET / ")) is type(None)


# 6
def test_request_init_wrong_type():
    with pytest.raises(BadRequestError):
        request_string_to_object("DOWNLOAD /movie.mp4 HTTP1.1")


# 7
def test_request_init_wrong_http():
    with pytest.raises(BadHTTPVersion):
        request_string_to_object("GET /movie.mp4 HTTP1.2")


# 8
def test_request_init_wrong_path():
    with pytest.raises(ValueError):
        request_string_to_object("GET movie.mp4 HTTP1.1")
