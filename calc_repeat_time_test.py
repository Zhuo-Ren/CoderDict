import datetime3 as datetime
from calc_repeat_time import  calc_b_time

# 单元测试
tasks = {
    ("apple", "拼"): {
        "log": [
                (0, datetime.datetime(1992, 1, 10, 23, 56), -1),  # 在92年1月10日23点56分添加到复习列表。
                # 计划于1分钟后（92年1月10日11点57分）进行下一次复习
                (1, datetime.datetime(1992, 1, 10, 23, 59), 4),  # 在92年1月11日10点03分完成复习进度1（第一次复习）, 考试得4分。
                # 计划于5分钟后（92年1月11日0点4分）进行下一次复习
            ],
        "next_index": 2,
        "next_time": datetime.datetime(1992, 1, 11, 0, 4)
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
# 如果我在19920111 0:3 对(apple, 拼)进行了复习，并得到4分
cur_task = tasks[("apple", "拼")]
cur_time = datetime.datetime(1992, 1, 11, 0, 3)
r = calc_b_time(log=cur_task["log"], B_index=cur_task["next_index"], b_time=cur_task["next_time"], B_time=cur_time, q=4)
print(r)

# 如果我在19920111 10:15 对(apple, 拼)进行了复习，并得到4分
cur_task = tasks[("apple", "拼")]
cur_time = datetime.datetime(1992, 1, 11, 10, 15)
r = calc_b_time(log=cur_task["log"], B_index=cur_task["next_index"], b_time=cur_task["next_time"], B_time=cur_time, q=4)
print(r)

# 如果我在19921004 10:5 对(apple, 认)进行了复习，并得到2分
cur_task = tasks[("apple", "认")]
cur_time = datetime.datetime(1992, 10, 4, 10, 5)
r = calc_b_time(log=cur_task["log"], B_index=cur_task["next_index"], b_time=cur_task["next_time"], B_time=cur_time, q=2)
print(r)
