from typing import Dict, List, Tuple, Union, Optional  # for type hinting
import datetime3 as datetime
import random
#
from calc_repeat_time import calc_b_time
import config


def finish_a_question(task_tuple: Tuple[str, str], time: datetime.datetime, score: float) -> None:
    """
    用户完成一个问题后，这个函数负责加以记录，并计算下一次复习计划。

    - 本次作答的信息被添加到tasks[对应任务][log].
      - (本次任务的序号, 本次任务的真实完成时间, 本次任务的作答得分)
    - 下次复习的计划信息被添加到tasks[对应任务]["next_index"]和["next_time"].
      - next_index: 下次复习的任务序号。
      - next_time: 下次复习的计划时间。

    :param task_tuple: 被完成的question所对应的的task的task tuple。
    :param time: 问题的完成时间。
    :param score: 问题的得分。
    :return: No return. But the global variable *tasks* is changed.
        本次作答的信息被添加到tasks[对应任务][log].
        下次复习的计划信息被添加到tasks[对应任务]["next_index"]和["next_time"].
    """
    task_info = config.tasks[task_tuple]
    log = task_info["log"]
    B_index = task_info["next_index"]
    b_time = task_info["next_time"]
    B_time = time
    # 计算下次复习
    (C_index, c_time) = calc_b_time(log=log, B_index=B_index, b_time=b_time, B_time=B_time, q=score)
    task_info["next_index"] = C_index
    task_info["next_time"] = c_time
    # 记录这次复习
    task_info["log"].append((B_index, B_time, score))


def get_all_activate_tasks(cur_time) -> List[Tuple[str, str]]:
    """
    获取当前所有需要复习的任务

    exampl::
    >>> get_all_activate_tasks(datetime.datetime(1992, 1, 10, 19, 32))
    [("apple", "拼"), ("apple", "听"), ("dog", "拼")]

    :param cur_time: Current time.
    :return: A list of all activated task tuple.
    """
    r = []
    for task_tuple, task_info in config.tasks.items:
        is_activate = cur_time < task_info["b_time"]
        if is_activate:
            r.append(task_tuple)
    return r


def get_unit_tasks(cur_time, max_tasks_num) -> List[Tuple[str, str]]:
    """
    从当前所有激活任务中，选择最多max_tasks_num个任务作为一个任务单元（用于生成一个试卷）。
    Get a unit of tasks that should be do at that moment.

    example::
    >>> get_unit_tasks(datetime.datetime(1992, 1, 10, 23, 11), 5)
    [
        ("apple", "拼"), ("apple", "认"), ("dog", "听"), ("pig", "拼")
    ]

    :param cur_time: Current time.
    :param max_tasks_num: How many tasks can be in one unit at most.
    :return: A sorted dict that represents a unit of tasks.
        A key is the entry spelling of the task.
        A value is the type of the task. Choose from config.py config["review task list"].
    """
    activate_tasks = get_all_activate_tasks(cur_time)
    if max_tasks_num <= len(activate_tasks):
        selected_index = random.sample(range(len(activate_tasks)), max_tasks_num)
    else:
        selected_index = random.sample(range(len(activate_tasks)), len(activate_tasks))
    selected_tasks = [activate_tasks[x] for x in selected_index]
    return selected_tasks


def task_to_question(task_entry, task_type):
    """
    Generate a question for a given task.
    example::
        >>> task_to_question("apple", "拼写")

    :param task_entry: Entry spelling of the given task.
    :param task_type: Type of the given task. Choose from config.py config["review task list"].
    :return:
    """
    pass
