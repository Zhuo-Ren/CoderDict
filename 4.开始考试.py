from typing import Dict, List, Tuple, Union, Optional  # for type hinting
from calc_repeat_time import  calc_b_time
import datetime3 as datetime
import config
from config import entries, crosses, tasks


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
    task_info = tasks[task_tuple]
    log = tasks["log"]
    B_index = task_info["next_index"]
    b_time = task_info["next_time"]
    B_time = time
    # 记录这次复习
    task_info["log"].append((B_index, B_time, score))
    # 计算下次复习
    (C_index, c_time) = calc_b_time(log=log, B_index=B_index, b_time=b_time, B_time=B_time, score)
    task_info["next_index"] = C_index
    task_info["next_time"] = c_time


# 单元测试
if 1:
    tasks = {
        ("apple", "拼"): {
            "log": [
                (0, datetime.datetime(1992, 1, 10, 23, 56), 5),  # 在92年1月10日23点56分添加到复习计划并学习。
                (1, datetime.datetime(1992, 1, 11, 10, 3), 4),  # 在92年1月11日10点03分完成复习进度1, 考试得分5分。
            ],
            "next_index": 2,
            "next_time": datetime.datetime(1992, 1, 11, 10, 8)
        },
        ("apple", "认"): {
            "log": [
                (0, datetime.datetime(1992, 9, 1, 13, 21), 5),  # 在92年1月10日23点56分添加到复习计划并学习。
                (1, datetime.datetime(1992, 9, 11, 10, 3), 4),  # 在92年1月11日10点03分完成复习进度1。
                (2, datetime.datetime(1992, 9, 12, 10, 3), 4),  # 在92年1月11日10点03分完成复习进度2。
                (3, datetime.datetime(1992, 9, 13, 10, 3), 5),  # 在92年1月11日10点03分完成复习进度3。
                (4, datetime.datetime(1992, 9, 14, 10, 3), 4),  # 在92年1月11日10点03分完成复习进度4。
                (5, datetime.datetime(1992, 9, 15, 10, 3), 5),  # 在92年1月11日10点03分完成复习进度5。
                (6, datetime.datetime(1992, 9, 19, 10, 3), 4),  # 在92年1月11日10点03分完成复习进度6。
                (7, datetime.datetime(1992, 9, 26, 10, 3), 4),  # 在92年1月11日10点03分完成复习进度7。
            ],
            "next_index": 8,
            "next_time": datetime.datetime(1992, 10, 3, 10, 3)
        }
    }
    # 如果我在19920111 10:5 对(apple, 拼)进行了复习，并得到4分
    cur_task = tasks[("apple", "拼")]
    cur_time = datetime.datetime(1992, 1, 11, 10, 5)
    r = calc_b_time(log=cur_task["log"], B_index=cur_task["next_index"], b_time=cur_task["next_time"], B_time=cur_time,
                    q=4)
    print(r)

    # 如果我在19920111 10:15 对(apple, 拼)进行了复习，并得到4分
    cur_task = tasks[("apple", "拼")]
    cur_time = datetime.datetime(1992, 1, 11, 10, 15)
    r = calc_b_time(log=cur_task["log"], B_index=cur_task["next_index"], b_time=cur_task["next_time"], B_time=cur_time,
                    q=4)
    print(r)

    # 如果我在19921004 10:5 对(apple, 认)进行了复习，并得到2分
    cur_task = tasks[("apple", "认")]
    cur_time = datetime.datetime(1992, 10, 4, 10, 5)
    r = calc_b_time(log=cur_task["log"], B_index=cur_task["next_index"], b_time=cur_task["next_time"], B_time=cur_time,
                    q=2)
    print(r)


def get_all_activate_tasks(cur_time, entries) -> List[Tuple[str, str]]:
    """
    获取当前所有需要复习的任务

    :param cur_time:
    :param entries:
    :return:
    """
    r = []
    for cur_entry in entries:
        is_activate = cur_time < cur_entry.b_time
        if is_activate:
            r.append(cur_entry)
    return r


def get_unit_tasks(cur_time, entries, max_tasks_num) -> List[Tuple[str, str]]:
    """
    获取当前需要复习的一组任务。
    Get a unit of review tasks that should be do at that moment based on the review strategy.

    example::
        return = {
            "apple": "拼写",
            "dog": "听力"
        }

    :param cur_time:
    :param cur_entry:
    :param cur_cross:
    :param max_tasks_num:
    :return: A sorted dict that represents a unit of tasks.
        A key is the entry spelling of the task.
        A value is the type of the task. Choose from config.py config["review task list"].
    """
    #
    activate_tasks = get_all_activate_tasks(cur_time, cur_entry, cur_cross)
    # 从activate_tasks中有序随机选max_question_num个
    unit_tasks = []
    score = []
    for i in range(len(activate_tasks)):
        score.append(random(0, 1))
    return unit_tasks

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
