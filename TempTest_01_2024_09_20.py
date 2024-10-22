'''
Author: xudawu
Date: 2024-09-20 09:11:00
LastEditors: xudawu
LastEditTime: 2024-10-22 18:01:49
'''
my_dict = {'key1': 1, 'key2': 2}
my_string = 'key1'

if 1 in my_dict:
    print("字符串在字典的键中")
else:
    print("字符串不在字典的键中")


my_dict['11']=3
print(my_dict.get('11'))