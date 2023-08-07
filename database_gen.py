# import re
import os
import json

def mkdir(path: str):
    path = path.strip()
    path = path.rstrip("/")
    if os.path.exists(path):
        print(f'path alread exists: {path}')
        return
    os.makedirs(path)

def strip_string(_str):
    two = _str.strip().strip('\r').strip('\n')
    result = ''
    for char in two:
        if (char != '\r') and (char != '\n') and (char != ' ') and (char != ' '):
            result = f'{result}{char}'
    return result

def str_k1a():
    string = """一二三
十木禾
上下土个
八入大天
人火文六
七儿九无
口日中
了子门月
不开四五
目耳头米
见白田电
也长山出
飞马鸟
云公车
牛羊小少
巾牙尺毛
卜又心风
力手水
广升足走
方半巴
业本平书
自已东西
回片皮
生里果
几用鱼
今正雨两
瓜衣来
年左右
万丁冬百齐
说话朋"""
    return strip_string(string)

def test1():
    chars = str_k1a()
    print(chars)
    print(f'There are {len(chars)} chars in total')
    unique_chars = set()
    for char in chars:
        unique_chars.add(char)
    print(f'There are {len(unique_chars)} unique chars in total')
    unique_string = ''
    for char in unique_chars:
        unique_string += char
    out_dir = '../p2h_data'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    out_file = os.path.join(out_dir, 'chars_k1a.json')
    chars_statics = {
        'k1a_chars_num': len(unique_chars),
        'k1a_chars': unique_string
    }
    with open(out_file, 'w', encoding='utf-8') as writer:
        json.dump(chars_statics, writer, indent=4, ensure_ascii=False)    

def main():
    # strip_str()
    test1()

if __name__ == "__main__":
    main()