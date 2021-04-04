import logging
import os
import string
from enum import Enum, auto
import json
import jsonschema
from jsonschema import validate


class ConfigReader:
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

    configuration = dict()
    _JSON_file_name = "json.txt"

    def create_config(self) -> dict:
        self.configuration["action on bad config"] = self.get_enum(self.ActionOnBadConfig, "What to do on bad input?")
        try:
            self.configuration["name of webserver log"] = input("What is the name of web server log?: ")
            self.configuration["requests"] = self.get_enum(self.Request,
                                                           "What type of HTTP requests to read (one or more separated by spaces)?",
                                                           True)
            self.configuration["logging level"] = self.get_enum(self.LoggingLevel, "What the logging level should be?")
            self.configuration["number of lines"] = self.get_int("How many lines should be displayed?")
            with open(self._JSON_file_name, "w") as write:
                json.dump(self.configuration, write)
        except self.UseOldException:
            self.read_old()
        return self.configuration

    # Method to ask user for input and accept only correct enums
    def get_enum(self, enum: iter, prompt: str, return_list: bool = False):
        # Loop repeats until the input is correct (until "return" is reached and executed)
        while True:
            value = input(prompt + " " + str([f"{e.name}/{e.value}" for e in enum]) + ": ")
            if return_list:
                try:
                    value = value.split()
                    return [enum[elem.upper()].name for elem in value]
                except KeyError:
                    self.handle_exception()
            else:
                try:
                    return enum[value.upper()].name
                except KeyError:
                    self.handle_exception()

    # Method to ask user for input and accept only integers
    def get_int(self, prompt: str) -> int:
        # Loop repeats until the input is correct (until "return" is reached and executed)
        while True:
            try:
                return int(input(prompt + ": "))
            except ValueError:
                self.handle_exception()

    # If user gives wrong value program quits, uses old config file *, or retries
    def handle_exception(self):
        if "action on bad config" not in self.configuration:
            action = self.ActionOnBadConfig.RETRY
        else:
            action = self.ActionOnBadConfig[self.configuration["action on bad config"]]
        print("WRONG INPUT")
        if action == self.ActionOnBadConfig.QUIT:
            print("QUITTING")
            quit(1)
        # * To use old file, method throws an exception which is caught by "add_config", to inform it to use old file
        elif action == self.ActionOnBadConfig.USE_OLD:
            raise self.UseOldException
        print('RETRY')

    def read_old(self):
        print("USING OLD CONFIG")
        with open(self._JSON_file_name, "r") as json_file:
            self.configuration = json.load(json_file)
        return self.configuration


class LogReader:

    def __init__(self, configuration):
        self.configuration = configuration
        if not self.check_config():
            print("wrong config")
        self.logging_setup()

    def check_config(self):
        config_schema = {"type": "object",
                         "properties": {
                             "action on bad config": {"type": "string"}
                         },
                         "required": ["action on bad config"],
                         "type": "object",
                         "properties": {
                             "name of webserver log": {"type": "string"}
                         },
                         "required": ["name of webserver log"],
                         "type": "array",
                         "properties": {
                             "requests": {
                                 "items": {
                                     "type": "string",
                                     "enum": [enum.value for enum in ConfigReader.Request]},
                             }
                         },
                         "required": ["requests"],
                         "type": "object",
                         "properties": {
                             "logging level": {
                                 "type": "string",
                                 "enum": [enum.value for enum in ConfigReader.Request]},
                         },
                         "required": ["logging level"],
                         "type": "object",
                         "properties": {"number of lines": {"type": "number"}
                                        },
                         "required": ["number of lines", "requests"],

                         }
        try:
            validate(instance=self.configuration, schema=config_schema)
            print("correct")
        except jsonschema.exceptions.ValidationError as err:
            print("error")
            print(err)
            return False
        return True

    def logging_setup(self):
        format_log = "[%(filename)s:%(lineno)s - %(funcName)20s()\t%(levelname)s\t] %(message)s"
        logging.basicConfig(level=self.configuration["logging level"], format=format_log)

    def read_log(self):
        data = dict[str, list[dict()]]()
        with open(self.configuration["name of webserver log"]) as file:
            for line in file:
                words = line.split()
                entry = {
                    "ip": str(words[0]),
                    "date": words[3][1:-1],
                    "request": str(words[5:7]),
                    "response code": words[8]
                }
                # TODO: requests is a list
                if entry["request"].upper() == self.configuration["requests"].upper():
                    if entry["ip"] in data:
                        data[entry["ip"]].append(entry)
                    else:
                        data[entry["ip"]] = [entry]
        return data


def run():
    reader = ConfigReader()
    configuration = reader.read_old()
    print(configuration)
    reader = LogReader(configuration)


if __name__ == "__main__":
    run()
