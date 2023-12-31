import os
import copy
from opencc import OpenCC
from pyjsonlib import  load_json, dump_json
from pyiolib import makedirs


def t2s(chars):
    cc = OpenCC('t2s')  # 使用OpenCC转换繁体为简体
    return cc.convert(chars)

def s2t(chars):
    cc = OpenCC('s2t')  # 使用OpenCC转换简体为繁体
    return cc.convert(chars)

def list2simple(_list: list):
    return [
        t2s(member) if type(member) is str else member
        for member in _list]

def dict2simple(poet: dict):
    new_poet = copy.deepcopy(poet)
    for key, value in poet.items():
        if type(value) is str:
            new_value = t2s(value)
            new_poet[key] = new_value
        elif type(value) is list:
            new_poet[key] = list2simple(value)
    return new_poet

def convert2simple(poets: list):
    return [dict2simple(poet) for poet in poets]

def s2t_group(words):
    for word in words:
        print(s2t(word))

def main():
    # https://zh.wiktionary.org/wiki/%E5%8A%92
    char = '劒'  # 剑劔劒劎剱剣
    print(t2s(char))  # 劒 -> 劒

    char = '犂'
    print(t2s(char))  # 犂 -> 犂

    char = '緌'
    print(t2s(char))

    char = '红'
    print(s2t(char))

    words = [
        '夜宿山寺',
        '楼'
        ]
    words = [
        '愤世少年行',
        '(清)陈中（十岁作',
        '人间自多不平事，善良常悲恶欺世。',
        '但等剑锋磨砺出，挑尽邪毒照晴日。'
        ]
    s2t_group(words)   


if __name__ =="__main__":
    main()