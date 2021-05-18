import random

import pytest

import lab10


# 1
def test_request_string_to_object_check_argument_type():
    with pytest.raises(TypeError):
        lab10.request_string_to_object(123)


# 2
def test_request_init_check_return_type():
    assert type(lab10.request_string_to_object("GET / HTTP1.1")) is lab10.Request


# 3
def test_request_init_check_variables():
    request = lab10.request_string_to_object("GET / HTTP1.1")
    assert request.type == "GET"
    assert request.path == "/"
    assert request.protocol == "HTTP1.1"


# 4
def test_request_init_check_variables_more():
        type = "POST"
        path = "/stupid.cat"
        protocol = "HTTP1.0"
        string = type + " " + path + " " + protocol
        request = lab10.request_string_to_object(string)
        assert request.type == type
        assert request.path == path
        assert request.protocol == protocol


# 5
def test_request_init_only_two_args():
    assert type(lab10.request_string_to_object("GET / ")) is type(None)


# 6
def test_request_init_wrong_type():
    with pytest.raises(lab10.BadRequestError):
        lab10.request_string_to_object("DOWNLOAD /movie.mp4 HTTP1.1")


# 7
def test_request_init_wrong_http():
    with pytest.raises(lab10.BadHTTPVersion):
        lab10.request_string_to_object("GET /movie.mp4 HTTP1.2")


# 8
def test_request_init_wrong_path():
    with pytest.raises(ValueError):
        lab10.request_string_to_object("GET movie.mp4 HTTP1.1")

