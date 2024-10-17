'''
Author: xudawu
Date: 2024-10-17 08:56:43
LastEditors: xudawu
LastEditTime: 2024-10-17 09:45:15
'''
import os

def read_txt_file(file_path):
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as file_reader:
        file_reader_list=[]
        # 逐行读取
        for line in file_reader.readlines():
            if line=='\n':
                continue
            temp_line=line
            # 去掉换行符号
            temp_line=temp_line.replace('\n', '')
            file_reader_list.append(temp_line)
    
    # 返回读取列表
    return file_reader_list

if __name__ == '__main__':
    # 获取当前文件路径
    file_base_path = os.getcwd()
    # 获得文件夹路径
    current_name_file_path = file_base_path+'\\current_name.txt'
    new_name_file_path = file_base_path+'\\new_name.txt'
    file_reader_current_list = read_txt_file(current_name_file_path)
    file_reader_new_list = read_txt_file(new_name_file_path)

    for name_index_int in range(len(file_reader_current_list)):
        # 获取原文件名和新的文件名
        current_file_name_str = file_reader_current_list[name_index_int]
        new_file_name_str = file_reader_new_list[name_index_int]

        # 使用 os.rename() 进行重命名
        try:
            os.rename(current_file_name_str, new_file_name_str)
            print(f'{current_file_name_str}文件已重命名为: {new_file_name_str}')
        except FileNotFoundError:
            print(f'文件 {current_file_name_str} 未找到。')
        except PermissionError:
            print(f'没有权限重命名文件 {current_file_name_str}。')
        except Exception as e:
            print(f'重命名文件时出错: {e}')
