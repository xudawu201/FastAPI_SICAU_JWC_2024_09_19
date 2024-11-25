'''
Author: xudawu
Date: 2024-11-06 16:28:23
LastEditors: xudawu
LastEditTime: 2024-11-25 14:20:36
'''
# 定义周、天和时间段
week_range = range(1, 3)  # 1到16周
day_range = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','sunday']  # 一周工作日
slot_per_day_range = range(1, 3)  # 每天4个时间段

# 初始化列表
timeslot_list = []

# 使用嵌套循环生成时间段
for week in week_range:
    for day in day_range:
        for slot in slot_per_day_range:
            timeslot = f"week:{week}, day:{day},slot:{slot}"
            timeslot_list.append(timeslot)

# 示例打印前几个时间段
for timeslot in timeslot_list:
    print(timeslot)
