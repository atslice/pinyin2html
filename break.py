import os
import copy
# from opencc import OpenCC
from pyjsonlib import  load_json, dump_json
from pyiolib import makedirs
from pyargslib import parse_args


def paragraphs_break(_list: list):
    new_p = []
    for member in _list:
        members = member.split('，', maxsplit=2)
        m1 = members[0] + '，'
        m2 = members[1]
        new_p.append(m1)
        new_p.append(m2)
    return new_p

def break_poet(poet: dict):
    new_poet = copy.deepcopy(poet)
    for key, value in poet.items():
        if key == 'paragraphs':  # value is list for such case
            if type(value) is list:
                new_poet['paragraphs_break'] = paragraphs_break(value)
    # new_poet["time_author"] = f'[{poet["time"]}] {poet["author"]}'
    return new_poet

def break_poets(poets: list):
    return [break_poet(poet) for poet in poets]

def main():
    # load input file
    # input_json = 'input/孟浩然_春.json'
    args = parse_args()
    # name = '古诗接龙'
    name = args.name

    input_json = f'input/{name}.json'
    print(f'input: {input_json}')
    poets = load_json(input_json) # list

    poets_break = break_poets(poets)

    out_dir = 'input/middle'
    makedirs(out_dir)
    out_file = os.path.join(out_dir, f'{name}_break.json')
    dump_json(_file=out_file, _dict=poets_break)
    print(f'break output: {out_file}')


if __name__ =="__main__":
    main()