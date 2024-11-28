'''
Author: xudawu
Date: 2024-11-06 16:28:23
LastEditors: xudawu
LastEditTime: 2024-11-28 14:40:44
'''
data = {}
key = "example"
value = "new_value"

# 添加数据到字典
if key in data:
    data[key].append(value)
else:
    data[key] = [value]

print(data)

key = "example"
value = "2"

if key in data:
    data[key].append(value)
else:
    data[key] = [value]

print(data)

for key, value in data.items():
    # print(key, value)
    for i in value:
        print(i)

