import os
import phyre
import phyre.interface.task.ttypes as task_if
import lzma


def load_compiled_task_dict():
    """Helper function to load the default task dump."""
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../../../data/tasks.bin.lzma")
    phyre_task = []
    task_map_all = {}
    with lzma.open(path) as stream:
        collection = phyre.simulator.deserialize(task_if.TaskCollection(),
                                                 stream.read())
        for task in collection.tasks:
            task_id = task.taskId
            task = task_id.split(":")
            task_template = task[0]
            task_mod = task[1]
            phyre_task.append(task)

            if task_template not in task_map_all:
                task_map_all[task_template] = []
            task_map_all[task_template].append(task_mod)
    return task_map_all, phyre_task
