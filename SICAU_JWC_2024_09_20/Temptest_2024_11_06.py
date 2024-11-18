'''
Author: xudawu
Date: 2024-11-06 16:28:23
LastEditors: xudawu
LastEditTime: 2024-11-18 10:06:04
'''
# 示例字典
data = {'a': 1, 'b': 2, 'c': 3}

# 删除键 'b' 并获取其值
removed_value = data.pop('b')
removed_value = data.pop('b')

c=str(data)

print(data)           # 输出: {'a': 1, 'c': 3}
print(removed_value)  # 输出: 2
print(c)