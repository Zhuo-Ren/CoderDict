import re

# findall会有损失的匹配。
a = re.findall(r'cc','''ccc''',re.I) 
print(a)  # ['cc']  第一第二个cc被匹配输出后，就算是消耗掉了。只省下第三个c，不能被匹配到。
a = re.findall(r'cc','''cccc''',re.I) 
print(a)  # ['cc', 'cc'] 第一第二个cc被匹配输出后，就算是消耗掉了。只省下第三个c和第四个c，还能被匹配一次。

# 忽略大小写
a = re.findall(r'Cc','''ccc''') 
print(a)  # 
a = re.findall(r'Cc','''ccc''',re.I) 
print(a)  # 

# 贪婪
print('贪婪')
#   默认贪婪
a = re.findall(
    r'\S+(?=[c])'  # r'(?<=CREATE TABLE\s\s)文件夹表(?=([(]| ))'
    ,'''1234567bcccc(de'''
) 
print(a)
#   在量词后加?转为非贪婪
a = re.findall(
    r'\S+?(?=[c])'  # r'(?<=CREATE TABLE\s\s)文件夹表(?=([(]| ))'
    ,'''1234567bcccc(de'''
) 
print(a)

# 转意
print('贪婪')
#   默认贪婪
a = re.findall(
    r'\S{2}(?=\()'  # r'(?<=CREATE TABLE\s\s)文件夹表(?=([(]| ))'
    ,'''1234567bcccc(de'''
) 
print(a)
#   在量词后加?转为非贪婪
a = re.findall(
    r'(?<=CREATE TABLE)\s*\S+?(?= |\()'  # r'(?<=CREATE TABLE\s\s)文件夹表(?=([(]| ))'
    ,'''CREATE TABLE 文件夹表1(    dsfdf   CREATE TABLE  文件夹表2 (   CREATE TABLE   文件夹表3 as tt (
        文件夹ID        INT       PRIMARY KEY         NOT NULL,
        文件夹路径      TEXT                          NOT NULL
    );'''
)
print(a)
print(a[0])
a = re.findall(r'\S+', a[0])
print(a)
print(a[0])