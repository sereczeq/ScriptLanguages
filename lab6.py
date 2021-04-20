import logging
import re
from enum import Enum


def run():
    reader = LogReader()
    # reader.read_config()
    # read_log()


def logging_setup(level):
    format_log = "[%(filename)s:%(lineno)s - %(funcName)20s()\t%(levelname)s\t] %(message)s"
    logging.basicConfig(level=level, format=format_log)


class LogReader:

    def __init__(self):
        self.display = {
            "lines": 1,
            "separator": " ",
            "filter": "HEAD",
        }

        self.LogFile = "lab4_log"
        self.log = []
        self.read_config()
        self.read_log()
        self.parse_log()
        self.print_from_subnet()

    def read_config(self):
        config = ""
        # all accept any amount of whitespace between lines
        # all assume that arguments are written below assimilated class
        # e.x. "[Config]" doesn't appear in between "name" and "LogFile"

        # accepts every character as a name
        log_file_regex = re.compile("\[LogFile\]\s*name=(?P<name>.*)")
        # accepts only capital letter as debug, later try catch to check if correct
        config_regex = re.compile("\[Config\]\s*debug=(?P<debug>[A-Z]+)")
        # arguments can be missing,
        # lines can be a number,
        # separator can be single character or a string contained in quotation marks e.x. "c0r /n re. cT !",
        # filter can contain only capital letters
        display_regex = re.compile(
            "\[Display\](\s|lines=(?P<lines>\d+)\s|separator=(?P<separator>(\"(?P<quotation>[\s\S]*?)\"|(?P<singleChar>.)))\s|filter=(?P<filter>[A-Z]+)\s)*")
        with open("lab6.config") as config_file:
            for line in config_file:
                config += line

        match = re.search(log_file_regex, config)
        if match:
            print(match.group("name"))
            self.LogFile = match.group("name")
        match = re.search(config_regex, config)
        if match:
            try:
                print(match.group("debug"))
                logging_setup(match.group("debug"))
            except:
                logging_setup("DEBUG")
        match = re.search(display_regex, config)
        if match:
            for string in ("lines", "separator", "filter"):
                if match.group(string):
                    self.display[string] = match.group(string)

    def read_log(self) -> [str]:
        try:
            with open(self.LogFile) as log_file:
                for line in log_file:
                    self.log.append(line)
            return self.log
        except FileNotFoundError:
            print("File {0} not found", self.LogFile)
            quit(1)

    def parse_log(self) -> [(str, str, str, str, str)]:
        #     IP, timestamp, request header, HTTP status code, size of the response
        regex = "(?P<ipAddress>(\d{1,3}\.){3}\d{1,3}) - - " \
                "(?P<timeStamp>\[\d{1,2}\/[A-Z][a-z]{2}\/\d{4}(:\d{2}){3} \+\d{4}]) " \
                "(?P<requestHeader>\"[A-Z]+? \/[-a-zA-Z0-9()@:%_\+.~#?&\/=]*? [A-Z]+?\/[\d.]+?\") " \
                "(?P<httpStatusCode>\d{3}) " \
                "(?P<sizeOfResponse>\d+?) "
        tuples = []
        for line in self.log:
            match = re.match(regex, line)
            if match:
                tuples.append((
                    match.group("ipAddress"),
                    match.group("timeStamp"),
                    match.group("requestHeader"),
                    match.group("httpStatusCode"),
                    match.group("sizeOfResponse"),
                ))
        return tuples

    def print_from_subnet(self, subnet="192.168.0.0"):
        mask_length = 254598 % 16 + 8

    def print_total_size(self):
        for line in self.log:
            

def does_ip_belong(ip, subnet_ip, mask_length):
        regex = re.compile("(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})")
        match = re.match(regex, subnet_ip)
        subnet_ip = ""
        for i in range(1, 5):
            subnet_ip += bin(int(match[i]))[2:]
        match = re.match(regex, ip)
        ip = ""
        for i in range(1, 5):
            ip += bin(int(match[i]))[2:]
        if ip[:mask_length] == subnet_ip[:mask_length] and int(ip[mask_length:],2) > int(subnet_ip[mask_length:],2):
            print("jej")




if __name__ == "__main__":
    does_ip_belong("192.168.12.12", "192.168.13.0", 16)
    run()
