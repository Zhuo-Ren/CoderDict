# 准备工作
- 下载[getDict](https://pan.baidu.com/share/link?uk=305151372&shareid=2565690867)
- 下载[牛津高阶英汉双解词典(第9版)的mdx文件和mdd文件](https://download.csdn.net/download/qq_36682526/12304563?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522159336452619195265959514%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=159336452619195265959514&biz_id=1&utm_medium=distribute.pc_search_result.none-task-download-2~all~top_click~default-3-12304563.ecpm_v1_rank_ctr_v4&utm_term=%E7%89%9B%E6%B4%A5%E9%AB%98%E9%98%B6%E8%8B%B1%E6%B1%89%E5%8F%8C%E8%A7%A3%E8%AF%8D%E5%85%B8)。
- 用getDict把mdx抽取为txt，再更改后缀为html;用getDict把mdd抽取得到css。具体参见[教程](http://www.ducidian.com/forum.php?mod=viewthread&tid=178)。

# 文件说明
- `raw/原版.html` 是从词典mdx中抽取得到的最原始的那个html文件
- `raw/原版debug.html` 是修改了`原版.html`中的如下bug：
  - lint词项内容有重复。
- `static/css/oalecd9.css` 是从词典mdd中抽取得到的css文件。
- `pkl/XXX.entry.pkl` 是对应XXX.py程序的输出文件，内容为一个字典对象entry_dict，保存词项数据。

    ```python
    entry_dict={
      spelling of the entry: {
          'html_raw': 原始html字符串, 
          # 这是词项对应的最原始的html，使用原始html标签
          # 不要改格式，用于改内容（例如添加例句）。
          'html': 改后的html字符串
          # 这是词项对应的修改后的html，逐渐改成自己定义的标签
          # 不要改内容，用于改格式。
          # 运行抽取函数后，就把html_raw中的内容抽取出来，转换成自定义的格式了。
          'test_log': [
            [datatime格式记录的第一次测试的时间, 整型的测试百分制得分],
            [datatime格式记录的第二次测试的时间, 整型的测试百分制得分],
            ...
          ]
      },
      ...
    }
    ```

- `pkl/XXX.cross.pkl` 是对应XXX.py程序的输出文件，内容为一个字典对象，保存跨词项的数据。
    ```python
    cross_dict={
      
    }
    ```

# 使用说明
- 运行`1.从html中提取原始词条.py`来初始化。此程序输入`raw/原版debug.html`，并按照词条拆分html，按字典的形式存储，最后持久化输出为`pkl/1.从html中提取原始词条.entry.pkl`和`pkl/1.从html中提取原始词条.cross.pkl`文件. 文件中的具体内容参见[文件说明中的解释](#文件说明)。
- 复制`pkl/1.从html中提取原始词条.entry.pkl`和`pkl/1.从html中提取原始词条.cross.pkl`为`pkl/entry.pkl`和`pkl/cross.pkl`。
- 运行`2.添加test_log.py`。
- 运行`2.添加html.py`。此程序会读取`pkl/entry.pkl`和`pkl/cross.pkl`，`entry_dict[每个词项][html_raw]`经过`raw_to_html`函数处理得到`entry_dict[每个词项][html]`，持久化回去。
- 运行`3.展示界面.py`来查看字典内容。此程序会读取指定pkl文件(默认是`pkl/entry.pkl`和`pkl/cross.pkl`)，并打开网页。修改url以指定你要查的单词。网页会展示l`entry_dict[指定词项][html]`和`entry_dict[指定词项][html——raw]`中的内容。
  - 点击“编辑”按钮修改字典内容，编辑后的内容保存到`entry_dict[当前词项][html_raw]`。html_raw更新了，那么html相应也要更新：`entry_dict[当前词项][html_raw]`经过`raw_to_html`函数处理得到`entry_dict[当前词项][html]`。持久化回去。
- 如果修改更新了`raw_to_html`函数，那么再运行一次`2.添加html.py`文件，以更新`entry_dict[每个词项][html]`。

