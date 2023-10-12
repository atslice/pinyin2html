import os
# import copy
from poet2html import PoetPinyin2h
from pyjsonlib import  load_json, dump_json
from pyiolib import makedirs, dump_str

def poets2html(out_dir, name, poets, final=False):
    """
        Args:
            out_dir: str, the path to store to result files
            name: str, the basename of file without extension
            poets: list of dict
            final: boolean, if True, it means each poet in poets contains the pinyin data, it is safe to read pinyin data from poets, and should not call pinyin lib to generate pinyin data            
        Example:
    [   {
        "author": "孟浩然",
        "paragraphs": [
            "春眠不覺曉，處處聞啼鳥。",
            "夜來風雨聲，花落知多少。"
        ],
        "tags": [
            "唐诗三百首",
            "春",
            "写景",
            "一年级下册",
            "惜春",
            "五言绝句",
            "小学古诗"
        ],
        "title": "春曉",
        "id": "cb168b3b-d104-4df7-9868-1e1225ddb941"
        },
    ]
    """
    p2h = PoetPinyin2h()
    p2h.gen_poets_html(poets=poets, final=final)

    out_file = os.path.join(out_dir, f'{name}_繁体版.html')
    dump_str(_file=out_file, _str=p2h.html_t)

    out_file = os.path.join(out_dir, f'{name}_简体版.html')
    dump_str(_file=out_file, _str=p2h.html_s)

    out_file = os.path.join(out_dir, f'{name}_繁简对照打印版.html')
    dump_str(_file=out_file, _str=p2h.html_cts)  

    heteronym_json = os.path.join(out_dir, f'{name}_heteronym.json')
    dump_json(_file=heteronym_json, _dict=p2h.heteronym)

    poets_pinyin_json = os.path.join(out_dir, f'{name}_pinyin.json')
    dump_json(_file=poets_pinyin_json, _dict=p2h.poets_pinyin)

    print(out_file)    

def json2html(out_dir, input_json, name, final=False):
    """
        final: boolean, if True, it means each poet in poets contains the pinyin data, it is safe to read pinyin data from poets, and should not call pinyin lib to generate pinyin data                
    """
    poets = load_json(input_json) # list
    poets2html(out_dir, name, poets, final)

def main():
    out_dir = '../p2h_data'
    makedirs(out_dir)    
    name = '古诗接龙_break_simple_add'
    input_json = f'input/middle/{name}.json'
    json2html(out_dir, input_json, name, final=False)    


if __name__ =="__main__":
    main()