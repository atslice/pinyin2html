import os
import copy
from opencc import OpenCC
from pyjsonlib import  load_json, dump_json
from pyiolib import makedirs
from pyargslib import parse_args


def t2s(chars):
    cc = OpenCC('t2s')  # 使用OpenCC转换繁体为简体
    return cc.convert(chars)

def list2simple(_list: list):
    return [
        t2s(member) if type(member) is str else member
        for member in _list]

def dict2simple(poet: dict):
    new_poet = copy.deepcopy(poet)
    for key, value in poet.items():
        added_key = f'{key}_simple'
        if type(value) is str: 
            new_value = t2s(value)
            new_poet[added_key] = new_value
        elif type(value) is list:
            new_poet[added_key] = list2simple(value)
    return new_poet

def convert2simple(poets: list):
    return [dict2simple(poet) for poet in poets]

def main():
    args = parse_args()
    # name = '古诗接龙_break'
    name = args.name
    input_json = f'input/middle/{name}.json'
    poets = load_json(input_json) # list

    poets_simple = convert2simple(poets)

    out_dir = 'input/middle'
    makedirs(out_dir)
    out_file = os.path.join(out_dir, f'{name}_simple_add.json')
    dump_json(_file=out_file, _dict=poets_simple)
    print(f't2s_add output: {out_file}')


if __name__ =="__main__":
    main()