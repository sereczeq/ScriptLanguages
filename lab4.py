import logging
import string
import sys


def run():
    logs = read_log()
    print("ip and number of requests:", ip_requests_number(logs))
    print(ip_find(logs, False))
    print("longest request:", longest_request(logs))
    print("non existent:", non_existent(logs))


def logging_setup():
    format_log = "[%(filename)s:%(lineno)s - %(funcName)20s()\t%(levelname)s\t] %(message)s"
    logging.basicConfig(level=logging.NOTSET, format=format_log)


def read_log():
    data = dict[string, list[dict()]]()
    with open("lab4_log") as file:
        for line in file:
            words = line.split()
            entry = {
                "ip": str(words[0]),
                "date": words[3][1:-1],
                "request": str(words[5:7]),
                "response code": words[8]
            }
            if entry["ip"] in data:
                data[entry["ip"]].append(entry)
            else:
                data[entry["ip"]] = [entry]
    return data


def ip_requests_number(log: []) -> dict[string, int]:
    data = dict()
    for line in log:
        data[line] = len(log[line])
    return data


def ip_find(data, most_active: bool = True):
    out = []
    val = -sys.maxsize
    if most_active:
        for key, array in data.items():
            if len(array) > val:
                val = len(array)
                out = [key]
            elif len(array) == val:
                out.append(key)
    else:
        val = -val
        for key, array in data.items():
            if len(array) < val:
                val = len(array)
                print(array[0])
                out = [key]
            elif len(array) == val:
                out.append(key)
    return out


def longest_request(data):
    maximum = (0, "", "")
    for array in data.values():
        for entry in array:
            if len(entry["request"]) > maximum[0]:
                maximum = (len(entry["request"]), entry["request"], entry["ip"])
    return maximum[1:]


def non_existent(data):
    out = set()
    for array in data.values():
        for entry in array:
            if entry["response code"][0] != "2":
                out.add(entry["request"])
    return out


if __name__ == "__main__":
    run()
