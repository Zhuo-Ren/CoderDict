"""
通过循序执行的方式处理数据
"""
import _pickle as cPickle
import re
from ui import ui
from lxml import etree

html_file = open("原版debug.html","r", encoding="UTF-8")
f = html_file.read()
html_file.close()

# center data structure
oxford_adv_list = []

# separate each word/idiom
oxford_adv_list = f.split("</>")

# get the spelling
oxford_adv = {}
for i in oxford_adv_list:
    # the last of the list is empty string
    if i == "":
        continue
    # delete the \n at the start of i
    if i[0] == "\n":
        i = i[1:]
    # get the spelling and entries
    match = re.match('[\s\S]+?\n', i)
    spelling = match.group()[:-1]
    raw = i[match.regs[0][1]:]
    if spelling not in oxford_adv:
        oxford_adv[spelling] = {'raw': [], 'rest': []}
    oxford_adv[spelling]['raw'].append(raw)
    oxford_adv[spelling]['rest'].append(raw)

for cur_spell in oxford_adv.keys():
    for cur_entry_index in range(len(oxford_adv[cur_spell]['rest'])):
        cur_entry = oxford_adv[cur_spell]['rest'][cur_entry_index]
        # delete empty char at the start of cur_entry
        """there is no empty char
        match = re.match('^[\s]*', cur_entry)
        i = match.regs[0][1]
        if i != 0:
            oxford_adv[cur_spell]['rest'][cur_entry_index] = cur_entry[i:]
        """
        # delete head label in cur_entry
        if cur_entry[:6] == "<head>":
            oxford_adv[cur_spell]['rest'][cur_entry_index] = cur_entry[168:]
            """168 is the len of head label"""
        """check if there is <head> label missing
        search = re.search("<head>", cur_entry)
        if search is not None:
            pass
        """

# extract link info, and add it to ['link']
for cur_spell in oxford_adv.keys():
    oxford_adv[cur_spell]['link'] = []
    for cur_entry_index in range(len(oxford_adv[cur_spell]['rest'])-1, -1, -1):
        cur_entry = oxford_adv[cur_spell]['rest'][cur_entry_index]
        match = re.match('@@@[^\n]*?\n', cur_entry)
        if match is not None:
            end_index = match.regs[0][1]
            # add the link to ['link']
            oxford_adv[cur_spell]['link'].append(cur_entry[:end_index])
            # del the link from ['rest']
            oxford_adv[cur_spell]['rest'][cur_entry_index] = cur_entry[end_index:]
            # del cur_entry if it is empty
            if re.search("\S", oxford_adv[cur_spell]['rest'][cur_entry_index]) is None:
                del oxford_adv[cur_spell]['rest'][cur_entry_index]

# extract <div>, and add it into ['POS']
for cur_spell in list(oxford_adv.keys()):
    oxford_adv[cur_spell]['pos'] = []
    for cur_entry_index in range(len(oxford_adv[cur_spell]['rest'])-1, -1, -1):
        cur_entry = oxford_adv[cur_spell]['rest'][cur_entry_index]
        cur_tree = etree.HTML(cur_entry)
        cixing_tiaozhuan = cur_tree.xpath('//div[@class="cixing_tiaozhuan"]')
        if cixing_tiaozhuan != []:
            cixing_tiaozhuan = cixing_tiaozhuan[0]
            cixing_tiaozhuan.xpath('..')[0].remove(cixing_tiaozhuan)
        cixing_part_list = cur_tree.xpath('//div[@class="cixing_part"]')
        if cixing_part_list != []:
            for cur_cixing_part_index in range(len(cixing_part_list)-1, -1, -1):
                cur_cixing_part = cixing_part_list[cur_cixing_part_index]
                oxford_adv[cur_spell]['pos'].append(str(
                    etree.tostring(cur_cixing_part, encoding='utf-8'), encoding="utf-8"
                ))
                cur_cixing_part.xpath('..')[0].remove(cur_cixing_part)
        oxford_adv[cur_spell]['rest'][cur_entry_index] = str(
            etree.tostring(cur_tree, encoding='utf-8')[12:-15], encoding="utf-8"
        )
        # del cur_entry if it is empty
        if re.search("\S", oxford_adv[cur_spell]['rest'][cur_entry_index]) is None:
            del oxford_adv[cur_spell]['rest'][cur_entry_index]

# extract <h-g>, and add it into ['h-g']
for cur_spell in list(oxford_adv.keys()):
    oxford_adv[cur_spell]['h-g'] = []
    for cur_entry_index in range(len(oxford_adv[cur_spell]['rest'])-1, -1, -1):
        cur_entry = oxford_adv[cur_spell]['rest'][cur_entry_index]
        if cur_entry == '':
            continue
        cur_tree = etree.HTML(cur_entry)
        h_g = cur_tree.xpath('//h-g')
        if len(h_g) == 0:
            pass
        elif len(h_g) > 1:
            # more than one <h-g> label
            raise RuntimeError('多个h-g')
        elif len(h_g) == 1:
            # 一个词性<h-g>
            h_g = h_g[0]
            oxford_adv[cur_spell]["h-g"].append(str(
                etree.tostring(h_g, encoding='utf-8'), encoding="utf-8"
            ))
            h_g.xpath('..')[0].remove(h_g)
            oxford_adv[cur_spell]['rest'][cur_entry_index] = str(
                etree.tostring(cur_tree, encoding='utf-8')[12:-15], encoding="utf-8"
            )
        # del cur_entry if it is empty
        if re.search("\S", oxford_adv[cur_spell]['rest'][cur_entry_index]) is None:
            del oxford_adv[cur_spell]['rest'][cur_entry_index]


# extract <idm-g>, and add it into ['idm-g']
for cur_spell in list(oxford_adv.keys()):
    oxford_adv[cur_spell]['idm-g'] = []
    for cur_entry_index in range(len(oxford_adv[cur_spell]['rest'])-1, -1, -1):
        cur_entry = oxford_adv[cur_spell]['rest'][cur_entry_index]
        if cur_entry == '':
            continue
        cur_tree = etree.HTML(cur_entry)
        idm_g = cur_tree.xpath('//idm-g')
        if len(idm_g) == 0:
            pass
        elif len(idm_g) > 1:
            # more than one <idm-g> label
            print(cur_spell)
            raise RuntimeError('多个h-g')
        elif len(idm_g) == 1:
            # 一个习语框<idm-g>
            idm_g = idm_g[0]
            oxford_adv[cur_spell]["idm-g"].append(str(
                etree.tostring(idm_g, encoding='utf-8'), encoding="utf-8"
            ))
            idm_g.xpath('..')[0].remove(idm_g)
            oxford_adv[cur_spell]['rest'][cur_entry_index] = str(
                etree.tostring(cur_tree, encoding='utf-8')[12:-14], encoding="utf-8"
            )
        # del cur_entry if it is empty
        if re.search("\S", oxford_adv[cur_spell]['rest'][cur_entry_index]) is None:
            del oxford_adv[cur_spell]['rest'][cur_entry_index]

# extract <div class="seealso">, and add it into ['seealso']
for cur_spell in list(oxford_adv.keys()):
    oxford_adv[cur_spell]['seealse'] = []
    for cur_entry_index in range(len(oxford_adv[cur_spell]['rest'])-1, -1, -1):
        cur_entry = oxford_adv[cur_spell]['rest'][cur_entry_index]
        cur_tree = etree.HTML(cur_entry)
        seealso = cur_tree.xpath('//div[@class="seealso"]')
        if seealso != []:
            seealso = seealso[0]
            seealso.xpath('..')[0].remove(seealso)
            oxford_adv[cur_spell]['seealse'].append(str(
                etree.tostring(seealso, encoding='utf-8'), encoding="utf-8"
            ))
            oxford_adv[cur_spell]['rest'][cur_entry_index] = str(
                etree.tostring(cur_tree, encoding='utf-8')[12:-15], encoding="utf-8"
            )
        # del cur_entry if it is empty
        if re.search("\S", oxford_adv[cur_spell]['rest'][cur_entry_index]) is None:
            del oxford_adv[cur_spell]['rest'][cur_entry_index]

# extract <pv-g>, and add it into ['pv-g']
for cur_spell in list(oxford_adv.keys()):
    oxford_adv[cur_spell]['pv-g'] = []
    for cur_entry_index in range(len(oxford_adv[cur_spell]['rest'])-1, -1, -1):
        cur_entry = oxford_adv[cur_spell]['rest'][cur_entry_index]
        cur_tree = etree.HTML(cur_entry)
        pv_g = cur_tree.xpath('//pv-g')
        if pv_g != []:
            pv_g = pv_g[0]
            pv_g.xpath('..')[0].remove(pv_g)
            oxford_adv[cur_spell]['pv-g'].append(str(
                etree.tostring(pv_g, encoding='utf-8'), encoding="utf-8"
            ))
            oxford_adv[cur_spell]['rest'][cur_entry_index] = str(
                etree.tostring(cur_tree, encoding='utf-8')[12:-15], encoding="utf-8"
            )
        # del cur_entry if it is empty
        if re.search("\S", oxford_adv[cur_spell]['rest'][cur_entry_index]) is None:
            del oxford_adv[cur_spell]['rest'][cur_entry_index]

for cur_spell in list(oxford_adv.keys()):
    for cur_entry_index in range(len(oxford_adv[cur_spell]['rest'])):
        cur_entry = oxford_adv[cur_spell]['rest'][cur_entry_index]
        if cur_entry == '':
            continue
        else:
            print(cur_spell)

try:
    for cur_spell in list(oxford_adv.keys()):
        for cur_entry_index in range(len(oxford_adv[cur_spell]['rest'])):
            cur_entry = oxford_adv[cur_spell]['rest'][cur_entry_index]
            if cur_entry == '':
                continue
            cur_tree = etree.HTML(cur_entry)
            h_g = cur_tree.xpath('//h-g')
            if len(h_g) == 0:
                pass
            elif len(h_g) > 1:
                # more than one <h-g> label
                raise RuntimeError('多个h-g')
            elif len(h_g) == 1:
                # 一个词性<h-g>
                h_g = h_g[0]
                sn_gs = h_g.xpath('./sn-gs')
                idm_gs_blk = h_g.xpath('./idm_gs_blk')
                if (len(sn_gs) == 0) & (len(idm_gs_blk) == 0):
                    # 一个词性<h-g>,没有解释<sn_gs>
                    pass
                elif len(sn_gs) > 1:
                    # 一个词性<h-g>,多个解释<sn_gs>
                    pass
                elif len(idm_gs_blk) > 1:
                    raise RuntimeError('more than one <idm_gs_blk>')
except:
    print(cur_spell)


# # read the pkl file
# with open('./dict.pkl', 'rb') as pkl_file:
#     oxford_adv = cPickle.load(pkl_file)

# output to pkl file
with open('./dict2.pkl', 'wb') as pkl_file:
    cPickle.dump(oxford_adv, pkl_file)

# ui(oxford_adv)
