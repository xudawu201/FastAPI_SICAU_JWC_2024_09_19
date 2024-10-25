'''
Author: xudawu
Date: 2024-09-12 16:00:37
LastEditors: xudawu
LastEditTime: 2024-10-25 11:18:36
'''

import pandas

# 按学号匹配等级
def match_first_second(excel_first_pandas,excel_second_pandas,first_row_name,second_row_name,new_column_name,new_column_name_form_second_file_str):

    # 锁定第一个文件中行指定内容
    temp_first_row_name_list = []
    for first_index, first_row in excel_first_pandas.iterrows():
        # 跳过空值
        if pandas.isnull(first_row[first_row_name])==True:
            continue
        # 只处理未处理过的行
        if first_row[first_row_name] not in temp_first_row_name_list:
            # 记录此行列名
            temp_first_row_name_list.append(first_row[first_row_name])
            # 锁定此行列的值
            temp_first_row_name_value = first_row[first_row_name]
        
            # 根据锁定的值在第二个文件中查找
            for second_index, second_row in excel_second_pandas.iterrows():
                if str(temp_first_row_name_value) == str(second_row[second_row_name]):
                    # 将匹配到的信息添加到第一个文件中
                    excel_first_pandas.at[first_index, new_column_name] = second_row[new_column_name_form_second_file_str]
                    print('first row {temp_first_row_name_value} content add:',second_row[new_column_name_form_second_file_str])
                    # 查询到后退出循环
                    break


def main():

    # # 读取 Excel 文件
    excel_first_path = 'asset\校级一流课程教学育人建设评审-评教.xlsx'
    excel_second_path = 'asset\师资基本信息.xls'
    # 第一个文件中要匹配的列名
    first_row_name = '负责人'
    # 第二个文件中要匹配的列名
    second_row_name = '姓名'
    # 添加新列名 'NewColumn'
    new_column_name = '教师'
    # 这个新列需要添加的属于第二个文件中的列名
    new_column_name_form_second_file_str = '教师编号'

    # 第二行为标题行
    excel_first_pandas = pandas.read_excel(excel_first_path,header=1)
    excel_second_pandas = pandas.read_excel(excel_second_path,header=0)

    # 第一个DataFrame添加新列
    excel_first_pandas[new_column_name] = None

    # 第一个第二个文件匹配并将匹配的数据添加到第一个excel文件新列中
    match_first_second(excel_first_pandas,excel_second_pandas,first_row_name,second_row_name,new_column_name,new_column_name_form_second_file_str)

    # 将修改后的 DataFrame 保存为新的 Excel 文件
    file_save_name='matched.xlsx'
    excel_first_pandas.to_excel(file_save_name, index=False)
    print(file_save_name,'saved')

if __name__ == '__main__':
    main()