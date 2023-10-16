from pyjsonlib import  load_json, dump_json
from pyiolib import makedirs, dump_str

# 程序一直在修改中， 重新生成的拼音并不智能(总是取第一个)，有的拼音已经手动修改，需要把修改后的拼音并进生成的结果中

def main():
    out_dir = '../p2h_data'
    makedirs(out_dir)    
    name = '古诗接龙_break_simple_add_pinyin'
    input_json = f'input/final/{name}.json'
    json2html(out_dir, input_json, name, final=True) 

    out_dir = '../p2h_data'
    makedirs(out_dir)    
    name = '古诗接龙_break_simple_add'
    input_json = f'input/middle/{name}.json'
    json2html(out_dir, input_json, name, final=False)        


if __name__ =="__main__":
    main()