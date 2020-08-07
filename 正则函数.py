import re

# 匹配------------------------------------------------------------------------

# re.match-匹配从字符串首开始，返回第一个成功的匹配。
print(re.match('www', 'www.runoob.com')) 
print(re.match('com', 'www.runoob.com')) 

# 匹配整个字符串(从首开始，到尾结束)
'''没有函数支持，但是你可以通过设定正则表达式以$结尾(表示匹配到尾结束)来指定匹配整个字符串'''
'''re.match就相当于在正则表达式的开头自带^(表示匹配从首开始)'''
print(re.match('www.runoob.com$', 'www.runoob.com')) 
print(re.match('com$', 'www.runoob.com')) 

# re.search-匹配任意位置，返回第一个成功的匹配。
print(re.search('www', 'www.runoob.com'))
print(re.search('com', 'www.runoob.com'))

# re.findall-匹配任意位置，返回所有成功的匹配（以迭代器形式）。
it = re.finditer(r"\d+", "12a32bc43jf3")
for match in it:
    print(match.group())  # <------------------------------------------输出匹配结果

# pattern.findall-匹配任意位置，返回所有成功的匹配（以列表形式），如果没有找到匹配的，则返回空列表。
pattern = re.compile(r'\d+')   # 相比于前边的几个方法，之后的方法必须有pattern调用，而不能直接调用
result1 = pattern.findall('runoob 123 google 456')
result2 = pattern.findall('run88oob123google456', 0, 10)

# 其他------------------------------------------------------------------------

# re.sub-替换字符串中的匹配项。
print(re.sub(r'-', "/", "2004-959-559"))

# re.split-按照能够匹配的子串将字符串分割后返回列表
print(re.split(r',', '1,234,567,89'))


