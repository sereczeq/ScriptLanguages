import logging
import re


class LogReader:

    def __init__(self):
        self.display = {
            "lines": 1,
            "separator": " ",
            "filter": "HEAD",
        }

        self.LogFile = "lab4_log"
        self.log = []
        self.tuples = []

    def read_config(self):
        config = ""
        # all accept any amount of whitespace between lines
        # all assume that arguments are written below assimilated class
        # e.x. "[Config]" doesn't appear in between "name" and "LogFile"

        # accepts every character as a name
        log_file_regex = re.compile("\\[LogFile]\\s*name=(?P<name>.*)")
        # accepts only capital letter as debug, later try catch to check if correct
        config_regex = re.compile("\\[Config]\\s*debug=(?P<debug>[A-Z]+)")
        # arguments can be missing,
        # lines can be a number,
        # separator can be single character or a string contained in quotation marks e.x. "c0r /n re. cT !",
        # filter can contain only capital letters
        display_regex = re.compile(
            "\\[Display](\\s|lines=(?P<lines>\\d+)\\s|separator=(?P<separator>(\"(?P<quotation>[\\s\\S]*?)\"|"
            "(?P<singleChar>.)))\\s|filter=(?P<filter>[A-Z]+)\\s)*")
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
            except ValueError:
                logging_setup("DEBUG")

        match = re.search(display_regex, config)
        if match:
            for string in ("lines", "filter"):
                group = match.group(string)
                if group:
                    self.display[string] = group
            group = match.group("singleChar")
            if group:
                self.display["separator"] = group
            group = match.group("quotation")
            if group:
                self.display["separator"] = group

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
        regex = "(?P<ipAddress>(\\d{1,3}\\.){3}\\d{1,3}) - - " \
                "(?P<timeStamp>\\[\\d{1,2}\\/[A-Z][a-z]{2}\\/\\d{4}(:\\d{2}){3} \\+\\d{4}]) " \
                "(?P<requestHeader>\"[A-Z]+? \\/[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*? [A-Z]+?\\/[\\d.]+?\") " \
                "(?P<httpStatusCode>\\d{3}) " \
                "(?P<sizeOfResponse>\\d+?) "
        for line in self.log:
            match = re.match(regex, line)
            if match:
                self.tuples.append((
                    match.group("ipAddress"),
                    match.group("timeStamp"),
                    match.group("requestHeader"),
                    match.group("httpStatusCode"),
                    match.group("sizeOfResponse"),
                ))
        return self.tuples

    def print_from_subnet(self, subnet="38.18.0.0"):
        mask_length = 254598 % 16 + 8
        count = 0
        for tup in self.tuples:
            ip = tup[0]
            if does_ip_belong(ip, subnet, mask_length):
                print(tup)
                count += 1
                if count == int(self.display["lines"]):
                    response = input("Do you want to continue? [Enter / NO]")
                    if response.upper() == "NO":
                        return
                    else:
                        count = 0

    def print_total_size(self):
        regex = re.compile("\"(?P<type>[A-Z]+?) ")
        total_size = 0
        for line in self.tuples:
            request_type = re.match(regex, line[2]).group("type")
            if request_type == self.display["filter"]:
                size = int(line[-1])
                total_size += size
                print(request_type, size, sep=self.display["separator"])
        print(total_size)


def does_ip_belong(ip, subnet_ip, mask_length):
    def to_bin(ip_to_convert):
        regex = re.compile("(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})")
        match = re.match(regex, ip_to_convert)
        ip_to_convert = ""
        for i in range(1, 5):
            ip_to_convert += bin(int(match[i]))[2:].zfill(8)
        return ip_to_convert

    subnet_ip = to_bin(subnet_ip)
    ip = to_bin(ip)

    # print(ip, ip[mask_length:], int(ip[mask_length:], 2), subnet_ip, subnet_ip[mask_length:],
    #       int(subnet_ip[mask_length:], 2), sep="\n")
    return ip[:mask_length] == subnet_ip[:mask_length] and int(ip[mask_length:], 2) > int(subnet_ip[mask_length:], 2)


def logging_setup(level):
    format_log = "[%(filename)s:%(lineno)s - %(funcName)20s()\t%(levelname)s\t] %(message)s"
    logging.basicConfig(level=level, format=format_log)


def run():
    reader = LogReader()
    reader.read_config()
    reader.read_log()
    reader.parse_log()
    reader.print_from_subnet()
    reader.print_total_size()


if __name__ == "__main__":
    run()

# pycodestyle output after first run:
# D:\Kod\Python>pycodestyle lab6.py
# lab6.py:26:80: E501 line too long (83 > 79 characters)
# lab6.py:30:80: E501 line too long (108 > 79 characters)
# lab6.py:33:80: E501 line too long (110 > 79 characters)
# lab6.py:75:80: E501 line too long (83 > 79 characters)
# lab6.py:77:80: E501 line too long (95 > 79 characters)
# lab6.py:78:80: E501 line too long (106 > 79 characters)
# lab6.py:132:80: E501 line too long (95 > 79 characters)
# lab6.py:134:80: E501 line too long (117 > 79 characters)
# lab6.py:138:80: E501 line too long (92 > 79 characters)

# I'm not going to print those errors, since my IDE is setup for 120 lines.
