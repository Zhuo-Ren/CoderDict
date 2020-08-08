from flask import Flask, render_template, request, jsonify
from typing import Dict, List, Tuple, Union  # for type hinting
import _pickle as cPickle
from raw_to_html import raw_to_html


def ui(
        entry_dict_path: str = "./pkl/1.从html中提取原始词条.entry.pkl",
        cross_dict_path: str = "./pkl/1.从html中提取原始词条.cross.pkl") -> None:
    """查看字典内容。

    This function read the given pkl file (`pkl/1.从html中提取原始词条.entry.pkl` and
    `pkl/1.从html中提取原始词条.cross.pkl` by default), and open web page。Edit url to search
    target word. The web page will show `entry_dict[指定词项][html]` and
    `entry_dict[指定词项][html_raw]`.

    :param entry_dict_path:
    :param cross_dict_path:
    """
    # read the pkl file
    with open(entry_dict_path, 'rb') as pkl_file:
        entry_dict = cPickle.load(pkl_file)
    with open(cross_dict_path, 'rb') as pkl_file:
        cross_dict = cPickle.load(pkl_file)

    app = Flask(__name__)

    @app.route('/view/', methods=["GET"])
    def init():
        entry = request.args.get("q")
        html = entry_dict[entry]['html']
        raw = entry_dict[entry]['html_raw']
        return render_template("main.html",
                               entry=entry,
                               raw=html,
                               html=html)

    @app.route('/edithtml', methods=["POST"])
    def edit_html():
        # save the new html_raw
        entry = request.form.get("entry")
        entry_dict[entry]['html_raw'] = request.form.get("raw")
        entry_dict[entry]['html'] = raw_to_html(entry, entry_dict[entry]['html_raw'])

        # save into pkl file
        with open('./pkl/3.1.去掉例句中的a标签.entry.pkl', 'wb') as pkl_file:
            cPickle.dump(entry_dict, pkl_file)

        # update the website
        return jsonify(True)

    print("http://127.0.0.1:5001/view/?q=good")
    app.run(port=5001)
