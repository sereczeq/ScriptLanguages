import logging
import sys


logging.basicConfig(level=logging.NOTSET)
data = []
path = "log.txt"
logging.info("START")
if len(sys.argv) == 2:
    path = sys.argv[1]
    logging.info("using cmd input")
else:
    logging.info("using predefined path")

try:
    logging.info(f"trying to access {path}")
    with open(path) as file:
        logging.info("file opened")
        for line in file:
            logging.debug(line)
            words = line.split()
            data.append({
                "path": words[0],
                "code": words[1],
                "bytes": int(words[2]),
                "millis": int(words[3])
            })
except Exception as e:
    print("Couldn't find file, exiting")
    logging.error("Couldn't open a file", e)
    exit(1)

print("All paths:")
for line in data:
    print(("!" if line["code"] == "404" else "") + line["path"])

largest = None
for line in data:
    line["bytes"] = 2
    if largest is None:
        largest = line
        logging.debug("largest is not none")
    if line["bytes"] > largest["bytes"]:
        largest = line
        logging.debug("new largest", line)
if largest is None:
    logging.error("largest is empty")
else:
    print("Largest resource's path:", largest["path"], "and processing time:", largest["millis"])

number_of_failed = 0
sum_of_bytes = 0
sum_of_processing_time = 0
for line in data:
    if line["code"] == "404":
        number_of_failed += 1
    sum_of_bytes += line["bytes"]
    sum_of_processing_time += line["millis"]
print("number of failed requests", number_of_failed)
print("sum of bytes", sum_of_bytes)
print("sum of kilobytes", sum_of_bytes/1000)
print("mean processing time", sum_of_processing_time/len(data) if len(data) > 0 else "No data")
logging.info("FINISH")
