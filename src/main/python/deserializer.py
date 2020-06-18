import sys
import json

def deserialize(path):
    task_info = None
    timestamp_info = []
    with open(path) as f:
        line = f.readline()
        task_info = deserialize_task(line)
        while line:
            line = f.readline()
            if line is not None and line != "":
                curr_timestamp = deserialize_timestamp(line)
                if curr_timestamp is not None:
                    timestamp_info.append(curr_timestamp)

    return task_info, timestamp_info

def deserialize_task(first_line):
    res = None
    if first_line is None or first_line == "":
        return res
    try:
        res = json.loads(first_line)
    except:
        print("Error:", sys.exc_info()[0])
        print("Malformed JSON")
    return res

def deserialize_timestamp(line):
    res = None
    if line is None or line == "":
        return res
    try:
        res = json.loads(line)
    except:
        print("Error:", sys.exc_info()[0])
        print("Malformed JSON")
    return res


if __name__ == '__main__':
    task_info, timestamp_info = deserialize(sys.argv[1])
    print(task_info)
    print(timestamp_info[0])
    print(timestamp_info[-1])
