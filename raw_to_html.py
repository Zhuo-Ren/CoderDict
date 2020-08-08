from lxml import etree

def raw_to_html(entry, html_raw):
    """
    输入一个entry的html_raw，输出它的html

    :param entry:
    :param html_raw:
    :return:
    """

    html = html_raw

    # 去掉例句中的<a>
    """<a href="x:word">word</a> 改成 word"""
    if 1:
        tree = etree.HTML(html)
        # get <x>
        liju_list = tree.xpath('//x')
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
        html = str(
            etree.tostring(tree[0][0], encoding='utf-8', method="html"), encoding="utf-8"
        )

    # return
    return html