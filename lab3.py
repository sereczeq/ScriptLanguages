import sys
import logging


def run():
    logging_setup()

    data = read_file()
    print(successful_reads(data))
    print(failed_reads(data))
    # print(html_entries(data))
    print_html_entries(data)


def logging_setup():
    format_log = "[%(filename)s:%(lineno)s - %(funcName)20s()\t%(levelname)s\t] %(message)s"
    logging.basicConfig(level=logging.NOTSET, format=format_log)


def read_file():
    data = []
    path = "log.txt"
    if len(sys.argv) == 2:
        path = sys.argv[1]

    logging.debug(f"trying to open file {path}")
    try:
        with open(path) as file:
            number_of_lines_read = 0
            number_of_empty_lines = 0
            for line in file:
                words = line.split()
                number_of_lines_read += 1
                if len(words) == 0:
                    number_of_empty_lines += 1
                    logging.info(f"Empty line number {number_of_empty_lines}")
                else:
                    path = words[0]
                    code = int(words[1])
                    size = int(words[2])
                    time = int(words[3])
                    data.append((path, code, size, time))
                    logging.debug(f"added: {data[-1]} to data")
            logging.debug(f"read {number_of_lines_read} lines and {number_of_empty_lines} were empty")

    except Exception as err:
        logging.error(f"Error reading file {path}. Error: {err}")
        print("Couldn't open the file, shutting down")
        exit(1)

    return data


def successful_reads(data):
    logging.info(f"data has {len(data)} entries")
    out = []
    for line in data:
        if str(line[1])[0] == "2":
            out.append(line)
        else:
            logging.debug(f"not successful read: {line}")
    logging.info(f"data has {len(out)} successful entries")

    return out


def failed_reads(data):
    logging.info(f"data has {len(data)} entries")
    out_four = []
    out_five = []
    for line in data:
        if str(line[1])[0] == "4":
            out_four.append(line)
        elif str(line[1])[0] == "5":
            out_five.append(line)
    logging.info(f"data has {len(out_four)} unsuccessful entries with code 4xx")
    logging.info(f"data has {len(out_five)} unsuccessful entries with code 5xx")

    out_four.extend(out_five)

    return out_four


def html_entries(data):
    logging.info(f"data has {len(data)} entries")
    out = []
    for line in successful_reads(data):
        if line[0].endswith(".html"):
            out.append(line)
    logging.info(f"data has {len(out)} successfully retrieved html pages")

    return out


def print_html_entries(data):
    print(html_entries(data))


if __name__ == "__main__":
    run()

# 9. All of the functions can be run multiple times, they're functions
