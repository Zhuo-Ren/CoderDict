import datetime3 as datetime


def calc_repeat_time(
        A_time, A_index,
        A_b,
        b_time, b_index,
        B_time,
        q,
):
    """
    A_index=-1, b_index=0 -> Bc=10s
    A_index=0,  b_index=1 -> Bc=30s

    :param A_time:
    :param A_index:
    :param A_b:
    :param b_time:
    :param b_index:
    :param B_time:
    :param q:
    :return:
    """
    ATime = A_time
    AIndex = A_index

    Ab = A_b
    AB = 0

    bTime = b_time
    bIndex = b_index
    BTime = B_time
    BIndex = 0

    Bc = 0
    cTime = 0
    cIndex = 0

    forget_list = [
        # 0 学习
        datetime.timedelta(seconds=10),
        # 1 第一次复习
        datetime.timedelta(seconds=30),
        # 2
        datetime.timedelta(minutes=2),
        # 3
        datetime.timedelta(minutes=5),
        # 4
        datetime.timedelta(minutes=30),
        # 5
        datetime.timedelta(hours=12),
        # 6
        datetime.timedelta(days=1),
        # 7
        datetime.timedelta(days=2),
        # 8
        datetime.timedelta(days=4),
        # 9
    ]

    提前复习 = True if BTime < bTime else False
    if 提前复习:
        """如果提前复习，那么复习计划b当做未完成，那么重复计划b"""
        BIndex = AIndex
        cIndex = bIndex
        Bc = Ab
        cTime = BTime + Bc
    else:
        """如果没有提起复习，那么一律当做完成了复习计划b，即使可能是比计划拖后很久才完成的。"""
        if 0 <= bIndex <= 8:
            """第1到9次复习的时间由艾宾浩斯遗忘曲线计算"""
            BIndex = bIndex
            cIndex = BIndex + 1
            Bc = forget_list[BIndex]
            cTime = BTime + Bc
        elif bIndex >= 9:
            """第10次以及之后的复习时间由M2算法计算"""
            if q < 3:
                BIndex = 0
                cIndex = 1
                Bc = forget_list[BIndex]
                cTime = BTime + Bc
            else:
                BIndex = bIndex
                cIndex = BIndex + 1
                Bc = Ab * EF
                cTime = BTime + Bc

    return (BTime,BIndex,Bc,cTime,cIndex)

