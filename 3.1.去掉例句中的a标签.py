"""
此程序会读取把`entry_dict[每个词项][html_raw]`复制到`entry_dict[每个词项][html]`，然后修改后者的格式。
"""
import _pickle as cPickle
import re
from lxml import etree


# read the pkl file
with open('pkl/1.从html中提取原始词条.entry.pkl', 'rb') as pkl_file:
    entry_dict = cPickle.load(pkl_file)
with open('pkl/1.从html中提取原始词条.cross.pkl', 'rb') as pkl_file:
    cross_dict = cPickle.load(pkl_file)

# copy html_raw to html
for cur_entry in entry_dict.keys():
    entry_dict[cur_entry]['html'] = entry_dict[cur_entry]['html_raw']
del cur_entry

# exact 例句
for cur_entry in entry_dict.keys():
    cur_html = entry_dict[cur_entry]['html']
    cur_tree = etree.HTML(cur_html)
    # get <x>
    liju_list = cur_tree.xpath('//x')
    for cur_liju in liju_list:
        for cur_element_index in range(len(cur_liju)-1, -1, -1):
            cur_element = cur_liju[cur_element_index]
            # get <a>
            """<a href="x:word">word</a> """
            if cur_element.tag == "a":
                if cur_element.attrib["href"][2:] == cur_element.text:
                    if cur_element.tail is None:
                        cur_word = cur_element.text
                    else:
                        cur_word = cur_element.text + cur_element.tail
                    if cur_element_index == 0:
                        if cur_liju.text is None:
                            cur_liju.text = cur_word
                        else:
                            cur_liju.text += cur_word
                    else:
                        if cur_liju[cur_element_index - 1].tail is None:
                            cur_liju[cur_element_index - 1].tail = cur_word
                        else:
                            cur_liju[cur_element_index - 1].tail += cur_word
                    cur_element.xpath('..')[0].remove(cur_element)
            del cur_element_index, cur_element
        del cur_liju
    entry_dict[cur_entry]['html'] = str(
        etree.tostring(cur_tree[0][0], encoding='utf-8'), encoding="utf-8"
    )
    del cur_entry, cur_html, cur_tree, liju_list

# output to pkl file
with open('./pkl/3.1.去掉例句中的a标签.entry.pkl', 'wb') as pkl_file:
    cPickle.dump(entry_dict, pkl_file)
with open('./pkl/3.1.去掉例句中的a标签.cross.pkl', 'wb') as pkl_file:
    cPickle.dump(cross_dict, pkl_file)
