'''
Author: xudawu
Date: 2024-11-06 16:28:23
LastEditors: xudawu
LastEditTime: 2024-12-04 15:42:15
'''
class MyClass:
    def __init__(self, value):
        self.value = value
        self.a = 0

# 创建类对象并存入列表
obj1 = MyClass(1)
obj2 = MyClass(2)
obj3 = MyClass(3)
my_list = [obj1, obj2, obj3]

print(my_list.index(obj2))

my_dict = {(1,2):obj1,(1,3):obj2,(1,4):obj3}

print(my_dict.get((1,3)))
print(my_list)
print('111',my_list[my_list.index(obj2)].a)

for (a,b),value in my_dict.items():
    print(b)
    value.value = 2
    value.a=1

print(my_dict.get((1,3)))
print(my_list)
print('111',my_list[my_list.index(obj2)].a)