"""
此程序会读取把`entry_dict[每个词项][html_raw]`复制到`entry_dict[每个词项][html]`，然后修改后者的格式。
"""
import _pickle as cPickle
from raw_to_html import raw_to_html

# read the pkl file
with open('pkl/1.从html中提取原始词条.entry.pkl', 'rb') as pkl_file:
    entry_dict = cPickle.load(pkl_file)
with open('pkl/1.从html中提取原始词条.cross.pkl', 'rb') as pkl_file:
    cross_dict = cPickle.load(pkl_file)

# go through the dict
for cur_entry in entry_dict.keys():
    entry_dict[cur_entry]['html'] = raw_to_html(cur_entry, entry_dict[cur_entry]['html_raw'])
del cur_entry

# output to pkl file
with open('./pkl/3.1.去掉例句中的a标签.entry.pkl', 'wb') as pkl_file:
    cPickle.dump(entry_dict, pkl_file)
with open('./pkl/3.1.去掉例句中的a标签.cross.pkl', 'wb') as pkl_file:
    cPickle.dump(cross_dict, pkl_file)
