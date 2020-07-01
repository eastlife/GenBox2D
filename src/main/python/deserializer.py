import sys
import json

def deserialize(path):
    task_info = None
    timestamp_info = []
    with open(path) as f:
        first_line = f.readline()
        task_info = deserialize_json(first_line)
        line = f.readline()
        action_info = deserialize_json(line)
        while line:
            line = f.readline()
            if line is not None and line != "":
                curr_timestamp = deserialize_json(line)
                if curr_timestamp is not None:
                    timestamp_info.append(curr_timestamp)

        solved_info = timestamp_info.pop()

    return task_info, action_info, timestamp_info, solved_info

def deserialize_json(line):
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
    task_info, action_info, timestamp_info, solved_info = deserialize(sys.argv[1])
    print(task_info)
    print(timestamp_info[0])
    print(timestamp_info[-1])
