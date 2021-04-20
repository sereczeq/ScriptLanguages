import logging
import os
from enum import Enum
import json


class ConfigReader:
    class UseOldException(Exception):
        """Breaks creating of config file and uses old one"""
        pass

    class Enums:
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

    _JSON_file_name = "config.json"

    def __init__(self):
        self.configuration = dict()
        self.create_config()

    def create_config(self) -> dict:
        self.configuration["action on bad config"] = self.get_enum(self.Enums.ActionOnBadConfig,
                                                                   "What to do on bad input?")
        try:
            self.configuration["name of webserver log"] = input("What is the name of web server log?: ")
            self.configuration["requests"] = self.get_enum(self.Enums.Request,
                                                           "What type of HTTP requests to read (one or more separated "
                                                           "by spaces)?",
                                                           True)
            self.configuration["logging level"] = self.get_enum(self.Enums.LoggingLevel,
                                                                "What the logging level should be?")
            self.configuration["number of lines"] = self.get_int("How many lines should be displayed (0 means all)?")

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
            action = self.Enums.ActionOnBadConfig.RETRY
        else:
            action = self.Enums.ActionOnBadConfig[self.configuration["action on bad config"]]
        print("WRONG INPUT")
        if action == self.Enums.ActionOnBadConfig.QUIT:
            print("QUITTING")
            quit(1)
        # * To use old file, method throws an exception which is caught by "add_config", to inform it to use old file
        elif action == self.Enums.ActionOnBadConfig.USE_OLD:
            raise self.UseOldException
        print('RETRY')

    def read_old(self):
        print("USING OLD CONFIG")
        try:
            with open(self._JSON_file_name, "r") as json_file:
                self.configuration = json.load(json_file)
        except json.JSONDecodeError as e:
            print("CONFIGURATION FILE NOT A JSON")
            print(e)
            print("TERMINATING PROGRAM")
            quit(1)
        return self.configuration


class LogReader:
    class LogReaderException(Exception):
        pass

    class WrongConfigSignature(LogReaderException):
        pass

    class WrongAction(LogReaderException):
        pass

    class LogFileNotExisting(LogReaderException):
        pass

    class WrongRequestType(LogReaderException):
        pass

    class WrongLoggingLevel(LogReaderException):
        pass

    class NotAnInteger(LogReaderException):
        pass

    data: dict[str, list[dict[str]]] = dict([])

    def __init__(self, path):
        try:
            with open(path, "r") as json_file:
                self.configuration = json.load(json_file)
                self.check_config()
        except self.LogReaderException as e:
            print("WRONG CONFIGURATION FILE")
            print(e)
            quit(1)
        except json.JSONDecodeError as e:
            print("CONFIGURATION FILE NOT A JSON")
            print(e.msg)
            print("TERMINATING PROGRAM")
            quit(1)
        self.logging_setup(ready=True)
        self.read_log()

    def check_config(self):
        if not ("action on bad config" in self.configuration and
                "name of webserver log" in self.configuration and
                "requests" in self.configuration and
                "logging level" in self.configuration and
                "number of lines" in self.configuration):
            raise self.WrongConfigSignature("Config file not containing proper attributes")

        if self.configuration["action on bad config"] not in ConfigReader.Enums.ActionOnBadConfig.__members__:
            raise self.WrongAction(f"\"{self.configuration['action on bad config']}\" is not proper action")

        if not os.path.exists(self.configuration["name of webserver log"]):
            raise self.LogFileNotExisting(f"file \"{self.configuration['name of webserver log']}\" does not exits")

        for elem in self.configuration["requests"]:
            if elem not in ConfigReader.Enums.Request.__members__:
                raise self.WrongAction(f"\"{elem}\" is not proper html request type")

        if not self.configuration["logging level"] in ConfigReader.Enums.LoggingLevel.__members__:
            raise self.WrongLoggingLevel(f"\"{self.configuration['logging level']}\" is not proper logging level")

        if type(self.configuration["number of lines"]) is not int:
            raise self.NotAnInteger(f"number of lines should be a number but it's not: "
                                    f"{self.configuration['number of lines']}")

    def logging_setup(self, ready=False):
        format_log = "[%(filename)s:%(lineno)s - %(funcName)20s()\t%(levelname)s\t] %(message)s"
        logging.basicConfig(level=ConfigReader.Enums.LoggingLevel[self.configuration["logging level"]].value if ready else logging.DEBUG, format=format_log)
        logging.debug(f'Logging level set to {ConfigReader.Enums.LoggingLevel[self.configuration["logging level"]].value if ready else logging.DEBUG}')

    def read_log(self):
        logging.debug(f'Opening {self.configuration["name of webserver log"]}...')
        with open(self.configuration["name of webserver log"]) as file:
            logging.debug(f'{self.configuration["name of webserver log"]} opened successfully')
            line_count = 0
            for line in file:
                line_count += 1
                words = line.split()
                entry = {
                    "ip": str(words[0]),
                    "date": words[3][1:-1],
                    "request": {"type": words[5][1:],
                                "resource": words[6],
                                "html thingy": words[7][:-1]},
                    "response code": words[8]
                }
                if entry["ip"] in self.data:
                    self.data[entry["ip"]].append(entry)
                else:
                    self.data[entry["ip"]] = [entry]
            logging.info(f'Read {len(self.data.keys())} ip addresses containing total of {line_count} requests')
        return self.data

    def print_index_html(self):
        data = dict()
        logging_matches_index = 0
        for key, array in self.data.items():
            for entry in array:
                # Check if resource contains "index"
                if "index" in entry["request"]["resource"]:
                    logging_matches_index += 1
                    # Format the data to print it properly in "display"
                    to_print = {"request": {"type": entry["request"]["type"], "resource": entry["request"]["resource"]}}
                    if key not in data:
                        data[key] = [to_print]
                    else:
                        data[key].append(to_print)
        logging.info(f'Found {logging_matches_index} matches')
        self.display(data)

    # For filtering the displayed data and displaying set amount of data at a time.
    def display(self, data: dict):
        logging.info(f'Displaying all requests containing any of: {self.configuration["requests"]}, showing {self.configuration["number of lines"]} at a time')
        logging_accepted = logging_rejected = 0
        counter = 0
        for array in data.values():
            for entry in array:
                # Loop for checking for request types
                for request in self.configuration["requests"]:
                    if request in entry["request"]["type"]:
                        logging_accepted += 1
                        # If for displaying only set amount of entries at a time
                        # If configured number is <= 0 display all uninterruptedly
                        if counter == self.configuration["number of lines"] and counter != 0:
                            counter = 0
                            # User can choose to stop displaying by typing "no"
                            logging.info("Asking user if they want to continue")
                            response = input("Do you want to continue? [Enter / no]").upper()
                            logging.debug(f'User inputted "{response}"')
                            if response.upper() == "NO":
                                logging.debug("Printing interrupted by user")
                                logging.info("Stopping to print on user request")
                                logging.info(f'Accepted {logging_accepted} requests, and rejected {logging_rejected}')
                                return
                        counter += 1
                        print(entry)
                    else:
                        logging_rejected += 1
        logging.debug("Printed all data successfully")
        logging.info(f'Accepted {logging_accepted} requests, and rejected {logging_rejected}')


def run():
    reader = ConfigReader()
    # configuration = reader.create_config()
    reader = LogReader("config.json")
    reader.print_index_html()
    # reader.display(reader.data)


if __name__ == "__main__":
    run()
