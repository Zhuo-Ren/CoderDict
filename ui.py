from flask import Flask, render_template, request, jsonify
from typing import Dict, List, Tuple, Union  # for type hinting
import _pickle as cPickle
from raw_to_html import raw_to_html
import datetime3 as datetime


def ui(
        entry_dict_path: str = "./pkl/entry.pkl",
        cross_dict_path: str = "./pkl/cross.pkl",
        memorize_dict_path: str = "./pkl/memorize.pkl"
       ) -> None:
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
    with open(memorize_dict_path, 'rb') as pkl_file:
        memorize_dict = cPickle.load(pkl_file)

    app = Flask(__name__)

    @app.route('/view/', methods=["GET"])
    def view():
        entry = request.args.get("q")
        html = entry_dict[entry]['html']
        raw = entry_dict[entry]['html_raw']
        if entry in memorize_dict:
            memo_obj_list = memorize_dict[entry]
        else:
            memo_obj_list = []
        return render_template("main.html",
                               entry=entry,
                               raw=html,
                               html=html,
                               memoObjList=memo_obj_list,
                               showType="view")

    @app.route('/learn/', methods=["GET"])
    def init():
        entry = request.args.get("q")
        html = entry_dict[entry]['html']
        raw = entry_dict[entry]['html_raw']
        if entry in memorize_dict:
            memo_obj_list = memorize_dict[entry]
        else:
            memo_obj_list = []
        return render_template("main.html",
                               entry=entry,
                               raw=html,
                               html=html,
                               memoObjList=memo_obj_list)

    @app.route('/edithtml', methods=["POST"])
    def edit_html():
        # save the new html_raw
        entry = request.form.get("entry")
        entry_dict[entry]['html_raw'] = request.form.get("raw")
        entry_dict[entry]['html'] = raw_to_html(entry, entry_dict[entry]['html_raw'])
            # save into pkl file
        with open(entry_dict_path, 'wb') as pkl_file:
            cPickle.dump(entry_dict, pkl_file)
        # update the website
        return jsonify(True)

    @app.route('/recordtest', methods=["POST"])
    def record_test():
        now = datetime.datetime.now()
        entry = request.form.get("entry")
        score = request.form.get("score")
        score = int(score)
        if not (0 < score < 100):
            raise RuntimeError("score的值不对")
        entry_dict[entry]['test_log'].append([now, score])
        # save into pkl file
        with open(entry_dict_path, 'wb') as pkl_file:
            cPickle.dump(entry_dict, pkl_file)
        # update the website
        return jsonify(True)


    print("http://127.0.0.1:5001/view/?q=good")
    app.run(port=5001)
