import _pickle as cPickle
import re
from ui import ui
from lxml import etree

def unbox_grammar_parse(html):
    e_id = re.search('(?<=e_id=")[\S]*(?=")', html)
    if e_id is None:
        raise RuntimeError('no e_id')
    e_id = e_id.group()
    association_dict[e_id] = html
    return e_id

def unbox_synonyms_parse(html):
    e_id = re.search('(?<=e_id=")[\S]*(?=")', html)
    if e_id is None:
        raise RuntimeError('no e_id')
    e_id = e_id.group()
    association_dict[e_id] = html
    return e_id
#  ----------------------------------------------------

# html_file = open("原版debug.html","r", encoding="UTF-8")
# f = html_file.read()
# html_file.close()
#
# # center data structure
# item_dict = {}
# association_dict = {}
#
# # separate each word/idiom
# item_list = f.split("</>")
# # get the spelling
# for i in item_list:
#     # the last of the list is empty string
#     if i == "":
#         continue
#     # delete the \n at the start of i
#     if i[0] == "\n":
#         i = i[1:]
#     # get the spelling and entries
#     match = re.match('[\s\S]+?\n', i)
#     spelling = match.group()[:-1]
#     raw = i[match.regs[0][1]:]
#     if spelling not in item_dict:
#         item_dict[spelling] = {'raw': [], 'rest': [], 'entries':[]}
#     item_dict[spelling]['raw'].append(raw)
#     item_dict[spelling]['rest'].append(raw)
# del item_list
#
# # delete <head>
# for cur_spell in item_dict.keys():
#     for cur_entry_index in range(len(item_dict[cur_spell]['rest'])):
#         cur_entry = item_dict[cur_spell]['rest'][cur_entry_index]
#         # delete empty char at the start of cur_entry
#         """there is no empty char
#         match = re.match('^[\s]*', cur_entry)
#         i = match.regs[0][1]
#         if i != 0:
#             oxford_adv[cur_spell]['rest'][cur_entry_index] = cur_entry[i:]
#         """
#         # delete head label in cur_entry
#         if cur_entry[:6] == "<head>":
#             item_dict[cur_spell]['rest'][cur_entry_index] = cur_entry[168:]
#             """168 is the len of head label"""
#         """check if there is <head> label missing
#         search = re.search("<head>", cur_entry)
#         if search is not None:
#             pass
#         """
#
# # extract link info
# for cur_spell in item_dict.keys():
#     item_dict[cur_spell]['link'] = []
#     for cur_entry_index in range(len(item_dict[cur_spell]['rest']) - 1, -1, -1):
#         cur_entry = item_dict[cur_spell]['rest'][cur_entry_index]
#         match = re.match('@@@[^\n]*?\n', cur_entry)
#         if match is not None:
#             end_index = match.regs[0][1]
#             # add the link to ['link']
#             item_dict[cur_spell]['entries'].append(['LINK', cur_entry[:end_index]])
#             # del the link from ['rest']
#             item_dict[cur_spell]['rest'][cur_entry_index] = cur_entry[end_index:]
#             # del cur_entry if it is empty
#             if re.search("\S", item_dict[cur_spell]['rest'][cur_entry_index]) is None:
#                 del item_dict[cur_spell]['rest'][cur_entry_index]
#
# # extract direct child in html format
# direct_child_type_set = set()
# for cur_spell in list(item_dict.keys()):
#     for cur_entry_index in range(len(item_dict[cur_spell]['rest'])):
#         cur_entry = item_dict[cur_spell]['rest'][cur_entry_index]
#         cur_tree = etree.HTML(cur_entry)
#         for i in range(len(cur_tree[0])):
#             cur_child = cur_tree[0][i]
#             cur_type = ""
#             cur_type += cur_child.tag
#             cur_type += (' ' + cur_child.attrib['class']) if 'class' in cur_child.attrib else ''
#             cur_type += (' ' + cur_child.attrib['type']) if 'type' in cur_child.attrib else ''
#             direct_child_type_set.add(cur_type)
#             item_dict[cur_spell]['entries'].append([
#                 cur_type,
#                 str(etree.tostring(cur_child, encoding='utf-8'), encoding="utf-8" )
#             ])
#     del item_dict[cur_spell]['rest']
# print(direct_child_type_set)  # {'h-g', 'unbox grammar', 'pv-g', 'dr-gs', 'id-g', 'div cixing_part', 'top-g', 'boxblock', 'subentry-g', 'div cixing_tiaozhuan', 'idm-g', 'br', 'unbox synonyms', 'div seealso'}

# read the pkl file
with open('./item.pkl', 'rb') as pkl_file:
    item_dict = cPickle.load(pkl_file)
with open('./association.pkl', 'rb') as pkl_file:
    association_dict = cPickle.load(pkl_file)

s = set()
#
for cur_spell in list(item_dict.keys()):
    for cur_entry_index in range(len(item_dict[cur_spell]['entries'])):
        cur_entry = item_dict[cur_spell]['entries'][cur_entry_index]
        # if cur_entry[0] == 'br':  # 空的，没用
        #     # 典型单词：clever。
        #     print('br:', cur_spell)
        #     # 更新本项
        #     item_dict[cur_spell]['entries'][cur_entry_index] = ['','']
        # if cur_entry[0] == 'unbox grammar':  # 语法框
        #     # 典型单词：hardly。
        #     print('g:', cur_spell)
        #     # 更新本项
        #     item_dict[cur_spell]['entries'][cur_entry_index] = [
        #         'GRAMMAR',
        #         unbox_grammar_parse(cur_entry[1])
        #     ]
        # if cur_entry[0] == 'unbox synonyms':  # 近义词
        #     # 典型单词：identify，thing。
        #     print('s:', cur_spell)
        #     # 更新本项
        #     item_dict[cur_spell]['entries'][cur_entry_index] = [
        #         'SYNONYMS',
        #         unbox_synonyms_parse(cur_entry[1])
        #     ]
        if cur_entry[0] == 'h-g':  # 单一词性框
            # 典型单词：3G,aback,...
            # print(cur_spell)
            cur_tree = etree.HTML(cur_entry[1])
            for i in range(len(cur_tree[0][0])):
                cur_child = cur_tree[0][0][i]
                cur_type = ""
                cur_type += cur_child.tag
                cur_type += (' ' + cur_child.attrib['class']) if 'class' in cur_child.attrib else ''
                cur_type += (' ' + cur_child.attrib['type']) if 'type' in cur_child.attrib else ''
                s.add(cur_type)
print(s)


# # output to pkl file
# with open('./item.o.pkl', 'wb') as pkl_file:
#     cPickle.dump(item_dict, pkl_file)
# with open('./association.o.pkl', 'wb') as pkl_file:
#     cPickle.dump(association_dict, pkl_file)

