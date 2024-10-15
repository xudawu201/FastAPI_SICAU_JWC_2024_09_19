'''
Author: xudawu
Date: 2024-09-29 11:21:28
LastEditors: xudawu
LastEditTime: 2024-10-15 11:34:52
'''

import pyodbc
import pandas

# DRIVER:驱动名称,SERVER:服务器名称,DATABASE:数据库名称,UID:用户名,PWD:密码
# cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=JWC_SCAU_2024_10_08;UID=sa;PWD=123')
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=jxgl_all;UID=sa;PWD=123')
# pyodbc使用微软的官方驱动ODBC driver对于中文的兼容性好，不需要再额外使用字符编码设置
# 创建游标对象
cursor = cnxn.cursor()


# 获得所有行数据
def get_all_rows(cursor):
    select_sql_str ='select * from aa毕业学生花名册'
    cursor.execute(select_sql_str)
    rows = cursor.fetchall()
    return rows

if __name__ == "__main__":

    # 执行SQL语句
    select_sql_str ='select * from aa毕业学生花名册'
    cursor.execute(select_sql_str)
    print(cursor)
    row = cursor.fetchone()
    print(row)

    cursor.execute(select_sql_str)
    row = cursor.fetchone()
    # 使用索引访问列数据
    print('name:', row[1])
    # 使用列名访问列数据
    print('name:', row.姓名)

    # 自定义一个列表
    # 假设列表包含字典，每个字典代表一行的数据
    target_data = [
        ['姓名','性别','学院'
        ],
    ]
 
    rows = get_all_rows(cursor)
    index =0
    for row in rows:
        index+=1
        print(f'index:{index}')
        
        # 添加数据
        temp_info_list=[]
        temp_info_list.extend([
            row.姓名,row.性别,row.系别
            ])
        print(f'{temp_info_list}')
        # 加入到总数据中
        target_data.append(temp_info_list)

    # 将列表整理为 DataFrame 格式
    # 提取标题和数据
    header = target_data[0]  # 取第一个列表元素作为标题
    data = target_data[1:]  # 剩余部分作为数据，需用[]包裹形成二维列表

    # 创建 DataFrame
    df = pandas.DataFrame(data, columns=header)

    # 保存为 Excel 文件
    output_file = 'sql_to_excel_test.xlsx'
    df.to_excel(output_file, index=False)

    print(f'文件已保存到 {output_file}')