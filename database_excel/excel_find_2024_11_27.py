'''
Author: xudawu
Date: 2024-09-12 16:00:37
LastEditors: xudawu
LastEditTime: 2024-11-27 19:23:36
'''

import pandas

# 人员类
class Person:
    def __init__(self, name,count=0):
        self.name_str = name
        self.count_int = count

# 按学号匹配等级
def excel_excute(excel_pandas,first_column_name,second_column_name,new_column_name):

    # 锁定第一个文件中行指定内容
    temp_row_name_list = []
    # 初始化人员列表
    Person_list = []
    for first_index, row in excel_pandas.iterrows():

        # 跳过空值
        if pandas.isnull(row[first_column_name])==True:
            continue

        # 只处理未处理过的行
        TempPerson_data = Person(row[first_column_name],0)
        temp_data = row[first_column_name]

        # 查找第一个列名中的内容进行操作
        if temp_data not in temp_row_name_list:
            # 更新人员列表
            Person_list.append(TempPerson_data)
            # 记录此行列名
            temp_row_name_list.append(temp_data)

        else:
            # 查找人员列表中此人
            for Person_data in Person_list:
                if str(temp_data) == str(Person_data.name_str):
                    # 更新此人计数
                    Person_data.count_int += 1

                    # 此人计数大于等于3则记录在新列中
                    if Person_data.count_int >=3 :
                        # 获取新列中的当前值（如果已有值，追加新内容）
                        current_value = temp_row_name_list.at[first_index, new_column_name]
                        if pandas.isnull(current_value):  # 如果当前值为空，直接写入
                            current_value = ''
                        # 追加新内容
                        new_value = f'{Person_data.name_str}:{Person_data.count_int+1}、'
                        temp_row_name_list.at[first_index, new_column_name] = current_value + new_value
                        break

        # 查找第二个列名中的内容进行操作
        # 获得值并去掉空格
        temp_data = row[second_column_name].replace(' ','')
        # 根据符号拆分
        temp_data_list = temp_data.split('、')
        # 遍历列表
        for temp_data in temp_data_list:
            if temp_data not in temp_row_name_list:
                # 更新人员列表
                TempPerson_data = Person(temp_data,0)
                Person_list.append(TempPerson_data)
                # 记录此行列名
                temp_row_name_list.append(temp_data)

            else:
                # 查找人员列表中此人
                for Person_data in Person_list:
                    if str(temp_data) == str(Person_data.name_str):
                        # 更新此人计数
                        Person_data.count_int += 1

                        # 此人计数大于等于3则记录在新列中
                        if Person_data.count_int >=2 :
                            # 获取新列中的当前值（如果已有值，追加新内容）
                            current_value = temp_row_name_list.at[first_index, new_column_name]
                            if pandas.isnull(current_value):  # 如果当前值为空，直接写入
                                current_value = ''
                            # 追加新内容
                            new_value = f'{Person_data.name_str}:{Person_data.count_int+1}、'
                            temp_row_name_list.at[first_index, new_column_name] = current_value + new_value
                            break

def main():

    # # 读取 Excel 文件
    excel_pandas = 'asset\附件3. 四川省2024-2026年高等教育人才培养质量和教学改革项目申报汇总表1126.xls'
    # 第一个列名
    first_column_name = '项目负责人（仅限1人）'
    # 第二个列名
    second_column_name = '项目组主要成员（不超过8位）'
    # 添加新列名 'NewColumn'
    new_column_name = '名字出现次数备注'

    # 第二行为标题行
    excel_first_pandas = pandas.read_excel(excel_pandas,header=3)

    # 第一个DataFrame添加新列
    excel_first_pandas[new_column_name] = None

    excel_excute(excel_pandas,first_column_name,second_column_name,new_column_name)

    # 将修改后的 DataFrame 保存为新的 Excel 文件
    file_save_name='添加名字出现次数_附件3. 四川省2024-2026年高等教育人才培养质量和教学改革项目申报汇总表1126.xlsx'
    excel_first_pandas.to_excel(file_save_name, index=False)
    print(file_save_name,'saved')

if __name__ == '__main__':
    main()