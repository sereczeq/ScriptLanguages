import logging
from datetime import datetime
import re


class WrongHTTPRequest(Exception):
    pass


class LogEntry:
    def __init__(self, entry: str):
        regex = "(?P<ipAddress>(\\d{1,3}\\.){3}\\d{1,3}) - - " \
                "(?P<timeStamp>\\[\\d{1,2}\\/[A-Z][a-z]{2}\\/\\d{4}(:\\d{2}){3} \\+\\d{4}]) " \
                "(?P<requestHeader>\"(?P<type>[A-Z]+?) (?P<resource>\\/[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*?)" \
                " [A-Z]+?\\/[\\d.]+)\" " \
                "(?P<httpStatusCode>\\d{3}) " \
                "(?P<sizeOfResponse>\\d+?) "

        match = re.match(regex, entry)
        if match:
            self.ipAddress = match.group("ipAddress")
            self.timeStamp = string_to_datetime(match.group("timeStamp"))
            self.requestHeader = RequestHeader(match.group("requestHeader"))
            self.httpStatusCode = match.group("httpStatusCode")
            self.sizeOfResponse = match.group("sizeOfResponse")
        else:
            raise WrongHTTPRequest(f'Wrong Entry: {entry}')

    def get_date(self) -> datetime:
        return self.timeStamp

    def __repr__(self) -> str:
        return f'Class Log Entry: {{\n\tIP address: {self.ipAddress},\n\t' \
               f'Time stamp: {self.timeStamp},\n\t' \
               f'Request Header: {self.requestHeader},\n\t' \
               f'HTTP status code: {self.httpStatusCode}, \n\t' \
               f'Size of the response: {self.sizeOfResponse}\n}}'


class RequestHeader:
    def __init__(self, request: str):
        regex = "(?P<requestHeader>\"?(?P<type>[A-Z]+?) (?P<resource>\\/[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*?)\"?" \
                " [A-Z]+?\\/[\\d.]+)"
        match = re.match(regex, request)
        if match:
            self.type = match.group("type")
            self.resource = match.group("resource")
        else:
            raise WrongHTTPRequest(f'Wrong Request Header: {request}')

    def __repr__(self):
        return f'Class Request Header {{ Header: "{self.type}", resource: "{self.resource}"}}'

    def get_type(self):
        return self.type

    def get_resource(self):
        return self.resource


def log_to_list_of_log_entry(name: str) -> [LogEntry]:
    list_of_entries = []
    i_logging = 1
    for line in read_log(name):
        try:
            list_of_entries.append(LogEntry(line))
        except WrongHTTPRequest as e:
            logging.error(f'Exception no.{i_logging}: {e}')
            i_logging += 1
    logging.debug(f'While reading log, found {i_logging} exceptions')
    return list_of_entries


def log_line_to_log_entry(line: str) -> LogEntry:
    return LogEntry(line)


def read_log(name) -> [str]:
    log = []
    try:
        with open(name) as log_file:
            for line in log_file:
                log.append(line)
        return log
    except FileNotFoundError:
        print("File {0} not found", name)
        quit(1)


def string_to_datetime(date: str) -> datetime:
    date_format = "[%d/%b/%Y:%H:%M:%S %z]"
    return datetime.strptime(date, date_format)


def requests_in_interval(requests: [LogEntry], date1: datetime, date2: datetime):
    if date1 > date2:
        print(f'ERROR: {date1} is later than {date2}, did you mean to pass them in reversed order?')
        return
    for request in requests:
        if date1 < request.get_date() < date2:
            print(request)


def logging_setup():
    format_log = "[%(filename)s:%(lineno)s - %(funcName)20s()\t%(levelname)s\t] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=format_log)


def run():
    file_name = "lab4_log"
    requests = log_to_list_of_log_entry(file_name)
    date1 = string_to_datetime("[18/Oct/2020:01:30:43 +0200]")
    date2 = string_to_datetime("[20/Oct/2020:01:30:43 +0200]")
    requests_in_interval(requests, date1, date2)


if __name__ == "__main__":
    run()
