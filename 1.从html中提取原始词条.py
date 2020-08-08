"""
本程序：
1.读取“原版debug.html”文件，并以</>为记号分割文件，得到block。
2.从block中分离出词项的spelling和htmlblock。
3.删除htmlblock中的<head>。
4.合并同一个entry的多个htmlblock,得到一个完整的html字符串。
3.构建【entry_dict】用于存放词项数据。
  entry_dict={
      spelling of the entry: {
          'html_raw': 词条对应的原始html,  # 只读
      },
      ...
  }
5.entry_dict持久化到pkl文件和sqlite数据库。
"""
import _pickle as cPickle
import re
from dbsql_sqlite import DbSql

# read the html file
html_file = open("raw/原版debug.html", "r", encoding="UTF-8")
f = html_file.read()
html_file.close()

# center data structure
entry_dict = {}
cross_dict = {}
"""
entry_dict用于存放词项数据。entry_dict的key是词项，value是这个词项对应的词项块组成的list。
大多数词项对应一个词项块，但是有个别的对应多个词项块。
"""

# split the file based on label </>, get block_list.
block_list = f.split("</>")
# the last element of block_list is empty string, del it
block_list = block_list[:-1]

# parse each block, get the spelling and htmlblock, and save them in entry_dict
for cur_htmlblock in block_list:
    # delete the \n at the start
    if cur_htmlblock[0] == "\n":
        cur_htmlblock = cur_htmlblock[1:]
    # get the spelling and htmlblock
    match = re.match('[\s\S]+?\n', cur_htmlblock)
    spelling = match.group()[:-1]
    htmlblock = cur_htmlblock[match.regs[0][1]:]
    if spelling not in entry_dict:
        entry_dict[spelling] = {'html_raw': []}
    else:
        print(spelling, "对应多个html块")
    entry_dict[spelling]['html_raw'].append(htmlblock)
del block_list, cur_htmlblock

# delete <head> in htmlblock
for cur_entry in entry_dict.keys():
    for cur_htmlblock_index in range(len(entry_dict[cur_entry]['html_raw'])):
        cur_htmlblock = entry_dict[cur_entry]['html_raw'][cur_htmlblock_index]
        # delete head label in cur_block
        if cur_htmlblock[:6] == "<head>":
            entry_dict[cur_entry]['html_raw'][cur_htmlblock_index] = cur_htmlblock[168:]
            """168 is the len of head label"""
        # check if there is <head> label missing
        search = re.search("<head>", cur_htmlblock)
        if search is not None:
            pass
        #
        del cur_htmlblock, cur_htmlblock_index
    del cur_entry

# combine htmlblocks of a entry to form a whole html string
for cur_entry in entry_dict.keys():
    html = ""
    for cur_htmlblock_index in range(len(entry_dict[cur_entry]['html_raw'])):
        cur_htmlblock = entry_dict[cur_entry]['html_raw'][cur_htmlblock_index]
        html += "<htmlblock>\n"
        html += cur_htmlblock
        html += "</htmlblock>\n"
    entry_dict[cur_entry]['html_raw'] = html
del html, cur_entry, cur_htmlblock_index, cur_htmlblock

# output to pkl file
with open('./pkl/1.从html中提取原始词条.entry.pkl', 'wb') as pkl_file:
    cPickle.dump(entry_dict, pkl_file)
with open('./pkl/1.从html中提取原始词条.cross.pkl', 'wb') as pkl_file:
    cPickle.dump(cross_dict, pkl_file)

# # output to sqlite
# try:
#     DbSql.connectDataBase('../dbsql_sqlite_test.sqlite')
#
#     DbSql.ensureTable(
#         tableName='entry_dict',
#         tableStructureInDict={
#             'entry': {'类型': '文本', '主键否': '主键'},
#             'html_raw': {'类型': '文本', '主键否': '非主键'},
#         },
#         updateStrategy='rewrite'
#     )
#     for cur_entry in entry_dict.keys():
#         DbSql.insertRow('entry_dict',
#                         {
#                             'entry': cur_entry,
#                             'html_raw': entry_dict[cur_entry]['html_raw'],
#                         }
#                        )
# finally:
#     DbSql.disconnectDataBase()


