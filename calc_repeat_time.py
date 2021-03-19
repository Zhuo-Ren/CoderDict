import datetime3 as datetime
from typing import Dict, List, Tuple, Union, Optional  # for type hinting


def calc_b_time(
        log: List[Tuple[int, datetime.datetime, float]],
        B_index: int, b_time: datetime.datetime,
        B_time: datetime.datetime, q: float) -> Tuple[int, datetime.datetime]:
    """
    用户做了一次复习，根据本次复习的情况，计算下次需要复习的时间。

    - -2: 上上次复习
    - A： 上次复习
    - b： 预计的本次复习
    - B： 真实的本次复习
    - c： 预计的下次复习

    :param log: 之前复习的记录
    :param B_index: 本次复习的进度序号
    :param b_time: 本次复习的预计时间
    :param B_time: 本次复习的真实时间
    :param q: 考试得分
    :return: (下次复习的进度序号, 下次复习的预计时间)
    """
    forget_list = [
        # 首次学习并添加到复习列表
        datetime.timedelta(minutes=1),
        # 1 第一次复习
        datetime.timedelta(minutes=5),
        # 2
        datetime.timedelta(minutes=30),
        # 3
        datetime.timedelta(hours=12),
        # 4
        datetime.timedelta(days=1),
        # 5
        datetime.timedelta(days=2),
        # 6
        datetime.timedelta(days=4),
        # 7
        datetime.timedelta(days=7),
        # 8
        datetime.timedelta(days=15),
        # 9
        datetime.timedelta(days=30),
        # 10
        datetime.timedelta(days=90),
    ]

    A_index: int = log[-1][0]
    """ 上次复习的进度序号。 """
    A_time = log[-1][1]
    """ 上次复习的完成时间。 """
    A_b: datetime.timedelta = b_time - A_time
    """ b_time - A_time """

    提前复习 = True if B_time < b_time else False
    if 提前复习:
        """如果提前复习，那么认为当前复习进度B未完成，那么重复计划b"""
        C_index = B_index
        B_c = A_b
        c_time = B_time + B_c
    else:
        """如果没有提前复习，那么认为当前复习进度B已完成，即使可能是比计划拖后很久才完成的。"""
        if 0 <= B_index <= 6:
            """前面的部分复习进度是定死的，无论用户的测试得分如何。"""
            C_index = B_index + 1
            B_c = forget_list[B_index]
            c_time = B_time + B_c
        else:  # 6 < B_index
            """后面的部分复习进度开始根据用户的记忆情况加以调整。"""
            if q > 3:
                "如果q大于3，则认为用户还记着这个词，根据记忆情况计算下次复习时间。"
                C_index = B_index + 1
                if B_index <= len(forget_list)-1:
                    B_c = forget_list[B_index]
                else:
                    B_c = forget_list[len(forget_list)-1]
                c_time = B_time + B_c
            else:
                "如果q小于3，则认为用户把这词全忘了，需要从头开始复习，复习进度归零。"
                C_index = 1
                B_c = forget_list[0]
                c_time = B_time + B_c
        """弃用
        "如果没有提前复习，那么认为当前复习进度B已完成，即使可能是比计划拖后很久才完成的。"
        if 0 <= B_index <= 6:
            "前面的部分复习进度时间由艾宾浩斯遗忘曲线计算"
            C_index = B_index + 1
            B_c = forget_list[B_index]
            c_time = B_time + B_c
        elif 6 < B_index:
            后面的复习进度时间由SM2算法计算：https://www.supermemo.com/en/archives1990-2015/english/ol/sm2
            if q < 3:
                "如果q小于3，则认为用户把这词全忘了，需要从头开始复习，复习进度归零。"
                C_index = 1
                B_c = forget_list[B_index]
                c_time = B_time + B_c
            else:
                "如果q大于3，则认为用户还记着这个词，根据记忆情况计算下次复习时间。"
                C_index = B_index + 1
                B_c = A_b * EF
                c_time = B_time + B_c
        """
    return C_index, c_time
