'''
Author: xudawu
Date: 2024-09-12 16:00:37
LastEditors: xudawu
LastEditTime: 2024-12-12 18:04:54
'''

import pandas

# 人员类
class Person:
    def __init__(self, name,count=0):
        self.name_str = name
        self.count_int = count
        self.is_flag = False

# 按学号匹配等级
def excel_excute(excel_pandas,first_column_name,second_column_name,new_column_name,excel2_pandas,excel2_column_name):

    # 锁定第一个文件中行指定内容
    temp_row_name_list = []
    # 初始化人员列表
    Person_list = []
    for first_index, row in excel_pandas.iterrows():

        # 跳过空值
        if pandas.isnull(row[first_column_name])==True:
            continue

        temp_data = row[first_column_name]

        # 查找第二个列名中的内容进行操作
        # 获得值并去掉空格
        temp2_data = row[second_column_name].replace(' ','')
        # 根据符号拆分
        temp_data_list = temp2_data.split('、')
        # 添加第一个名字
        temp_data_list.append(temp_data)
        
        # 新列要添加的名字
        add_name_str=''

        for index2, row2 in excel2_pandas.iterrows():
            # 跳过空值
            if pandas.isnull(row2[excel2_column_name])==True:
                continue
            
            cur_name_str = row2[excel2_column_name]
            if cur_name_str in temp_data_list:
                add_name_str+=cur_name_str+'、'

        # 将匹配到的信息添加到第一个文件中
        excel_pandas.at[first_index, new_column_name] = add_name_str
    
def main():

    # # 读取 Excel 文件
    excel_pandas = 'asset/附件2.2024-2026年省级教改项目信息核实清单.xlsx'
    excel2_pandas = 'asset\附件1.2024-2026年省级教改项目重复人员名单.xls'
    
    # 第一个列名
    first_column_name = '项目负责人（仅限1人）'
    # 第二个列名
    second_column_name = '项目组主要成员（不超过8位）'
    # 添加新列名 'NewColumn'
    new_column_name = '添加名字匹配'

    # 第0行为标题行
    excel_first_pandas = pandas.read_excel(excel_pandas,header=0)
    # 打印列名
    print(excel_first_pandas.columns)

    # 第2个文件
    excel2_pandas = pandas.read_excel(excel2_pandas,header=0)
    excel2_column_name = '重复人名'

    # 第一个DataFrame添加新列
    excel_first_pandas[new_column_name] = None

    excel_excute(excel_first_pandas,first_column_name,second_column_name,new_column_name,excel2_pandas,excel2_column_name)

    # 将修改后的 DataFrame 保存为新的 Excel 文件
    file_save_name='添加名字匹配_附件2.2024-2026年省级教改项目信息核实清单.xlsx'
    excel_first_pandas.to_excel(file_save_name, index=False)
    print(file_save_name,'saved')

if __name__ == '__main__':
    main()