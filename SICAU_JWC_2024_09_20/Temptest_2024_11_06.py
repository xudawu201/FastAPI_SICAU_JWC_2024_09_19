'''
Author: xudawu
Date: 2024-11-06 16:28:23
LastEditors: xudawu
LastEditTime: 2024-12-16 08:48:17
'''
import random

my_list = ['apple', 'banana', 'cherry', 'date']

# 使用 random.choices() 随机选择多个元素，可以重复选择
selected_elements_with_replacement = random.choices(my_list, k=2)
print("随机选中的元素（可重复）是:", selected_elements_with_replacement)

# 使用 random.sample() 随机选择多个元素，不重复选择
selected_elements_without_replacement = random.sample(my_list, k=2)
print("随机选中的元素（不重复）是:", selected_elements_without_replacement)