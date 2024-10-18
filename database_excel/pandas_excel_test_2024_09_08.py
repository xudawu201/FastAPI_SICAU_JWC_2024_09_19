'''
Author: xudawu
Date: 2024-09-08 19:12:50
LastEditors: xudawu
LastEditTime: 2024-09-08 20:04:27
'''
import pandas

# 测试数据
data = {'ID': [1, 2, 3], 'Name': ['张三', '李四', '王五']}

# 1.创建 DataFrame 对象
df = pandas.DataFrame(data=data)

# 可选操作。将 ID 设为索引，若不设置，会使用默认索引 narray(n)
df = df.set_index('ID')  # 写法1
# df.set_index('ID', inplace=True)  # 写法2

# 2.写入 excel 至指定位置（若文件已存在，则覆盖）
df.to_excel('Asset2021_10_23\\pandas_test.xlsx')

excel_path='Asset2021_10_23\\pandas_test_2024_09_08.xlsx'
# 默认0行为标题
excel_df = pandas.read_excel(excel_path)
# 场景2：excel 中第 2 行才是我们想要的标题（即：header=1）
# excel_df = pandas.read_excel(excel_path, header=1)
print(excel_df)
print('- '*10)

# 查看数据shape
print(excel_df.shape)
print('- '*10)

# 查看数据类型
print(excel_df.dtypes)
print('- '*10)

# 查看列名
print(excel_df.columns)
print('- '*10)

# 查看前几行数据
print('excel_df.head(3)','- '*10)
print(excel_df.head(3))

# 查看后几行数据
print('excel_df.tail(3)','- '*10)
print(excel_df.tail(3))

# 读取 Excel B - D 列（均包含）
excel_df = pandas.read_excel(excel_path, usecols='B:D')
print('excel_df','- '*10)
print(excel_df)

print('for item in excel_df','- '*10)
for item in excel_df:
    print(item)

# 读取第一行数据
print('excel_df.loc[0]','- '*10)
print(excel_df.loc[0])

# 读取第一行第一列数据
# print('excel_df.loc[0][0]','- '*10)
# print(excel_df.loc[0][0])

# 获取指定列
print('excel_df[''name'']','- '*10)
a=excel_df['name']
print(a)

# 遍历指定列
print('for item in a','- '*10)
for item in a:
    print(item)

# 获取索引为1的行，即第二行
print('excel_df.iloc[1]','- '*10)
print(excel_df.iloc[1])

# 获取索引切片的行，不包含末尾数字
print('excel_df.iloc[:2]','- '*10)
print(excel_df.iloc[:2])

# 获取指定行指定列的数据
print('excel_df.iloc[1,2]','- '*10)
print(excel_df.iloc[1,2])

# 获取范围指定行指定列
print('excel_df.iloc[1:2,1:2]','- '*10)
print(excel_df.iloc[1:2,1:2])