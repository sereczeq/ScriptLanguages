import string
from enum import Enum, auto
import json


class UseOldException(Exception):
    """Breaks creating of config file and uses old one"""
    pass


class Request(Enum):
    GET = 1
    HEAD = 2
    POST = 3
    PUT = 4
    DELETE = 5
    CONNECT = 6
    OPTIONS = 7
    TRACE = 8
    PATCH = 9


class LoggingLevel(Enum):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0


class ActionOnBadConfig(Enum):
    RETRY = 1
    QUIT = 2
    USE_OLD = 3


def run():
    add_config()


def add_config():
    _JSON_file_name = "json.txt"
    configuration = dict()
    configuration["action on bad config"] = get_enum(ActionOnBadConfig, "What to do on bad input?",
                                                     ActionOnBadConfig.RETRY)
    action = ActionOnBadConfig[configuration["action on bad config"]]
    try:
        configuration["name of webserver log"] = input("What is the name of web server log?: ")
        configuration["request"] = get_enum(Request, "What type of HTTP requests to read?", action)
        configuration["logging level"] = get_enum(LoggingLevel, "What the logging level should be?", action)
        configuration["number of lines"] = get_int("How many lines should be displayed?", action)
        with open(_JSON_file_name, "w") as write:
            json.dump(configuration, write)
    except UseOldException:
        print("USING OLD CONFIG")
        with open(_JSON_file_name, "r") as json_file:
            configuration = json.load(json_file)
    print(configuration)


# Method to ask user for input and accept only correct enums
def get_enum(enum: iter, prompt: str, action: ActionOnBadConfig) -> str:
    # Loop repeats until the input is correct (until "return" is reached and executed)
    while True:
        value = input(prompt + " " + str([f"{e.name}/{e.value}" for e in enum]) + ": ")
        value = value.upper()
        try:
            return enum[value].name
        except KeyError:
            handle_exception(action)


# Method to ask user for input and accept only integers
def get_int(prompt: str, action: ActionOnBadConfig) -> int:
    # Loop repeats until the input is correct (until "return" is reached and executed)
    while True:
        try:
            return int(input(prompt + ": "))
        except ValueError:
            handle_exception(action)


# If user gives wrong value program quits, uses old config file *, or retries
def handle_exception(action):
    print("WRONG INPUT")
    if action == ActionOnBadConfig.QUIT:
        print("QUITTING")
        quit(1)
    # * To use old file, method throws an exception which is caught by "add_config", to inform it to use old file
    elif action == ActionOnBadConfig.USE_OLD:
        raise UseOldException
    print('RETRY')


if __name__ == "__main__":
    run()
