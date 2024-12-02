'''
Author: xudawu
Date: 2024-11-06 16:28:23
LastEditors: xudawu
LastEditTime: 2024-12-02 14:26:08
'''
class MyClass:
    def __init__(self, value):
        self.value = value

# 创建类对象并存入列表
obj1 = MyClass(1)
obj2 = MyClass(2)
obj3 = MyClass(3)
my_list = [obj1, obj2, obj3]

# 基于类的属性值查找索引
target_value = 3
index = next((i for i, obj in enumerate(my_list) if obj.value == target_value), -1)
print(index)  # 输出 1

print(my_list.index(obj2))


for i in my_list:
    if i.value == 3:
        print(my_list.index(i))