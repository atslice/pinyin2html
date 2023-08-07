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
"""
    return strip_string(string)

def str_k1s():
    string = """万丁冬百齐
说话朋友春高
你们红绿花草
爷节岁亲的行
古声多处知忙
洗认扫真父母
爸全关写完家
看着画笑兴会
妈奶午合放收
女太气早去亮
和语千李秀香
听唱连远定向
以后更主意总
先干赶起明净
同工专才级队
蚂蚁前空房网
诗林童黄闭立
是朵美我叶机
她他送过时让
吗吧虫往得很
河姐借呢呀哪
谁怕跟凉量最
园因为脸阳光
可石办法找许
别到那都吓叫
再象像做点照
沙海桥竹军苗
井乡面忘想念
王从边这进道
贝原男爱虾跑
吹地快乐老师
短对冷淡热情
拉把给活种吃
练习苦学非常
问间伙伴共汽
分要没位孩选
北南江湖秋
只星雪帮请就
球玩跳桃树刚
兰各坐座带急
名发成晚动新
有在什么变条"""
    return strip_string(string)


def write_database(chars, name):
    """
        write to json file
        Args:
            chars: str
            name: str, the description, and will be used as key name and file basename without extension. 
        The result json file basename will be '{name}.json'.
        The result json will be in the format as below:
            {
                name:
                    {
                        'chars_num': int,
                        'chars': str
                    }
            }
    """

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

    out_file = os.path.join(out_dir, f'{name}.json')
    chars_statics = {
        name: {
            'chars_num': len(unique_chars),
            'chars': unique_string
        }
    }
    with open(out_file, 'w', encoding='utf-8') as writer:
        json.dump(chars_statics, writer, indent=4, ensure_ascii=False)    

def relation(str1, str2):
    """
        Args:
            str1: str
            str2: str
        Return: (str, str, str)
            (covered, uncovered, chars_over)
            covered: the chars which are both in str1 and str2 交集
            uncovered: the chars which are in str1 but not in str2
            chars_over: the chars which are in str2 but not in str1
    """
    covered = ''
    uncovered = ''    
    for char in str1:
        if char in str2:
            covered += char
        else:
            uncovered += char
    chars_over = ''
    for char in str2:
        if not char in str1:
            chars_over += char
    return covered, uncovered, chars_over

def test1():
    chars_k1a = str_k1a()
    write_database(chars=chars_k1a, name='k1a')
    chars_k1s = str_k1s()
    write_database(chars=chars_k1s, name='k1s')
    chars_k1 = chars_k1a + chars_k1s
    write_database(chars=chars_k1, name='k1')
    covered, uncovered, chars_over = relation(chars_k1a, chars_k1s)
    print(f'covered: {covered}')

def main():
    # strip_str()
    test1()

if __name__ == "__main__":
    main()