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

def load_string(_file):
    """
        load string from file
    """
    with open(_file, 'r') as reader:
        return reader.read()

def str_k12(name):
    """
        Args:
            name: str, the available values list ['k1a', 'k1s', 'k2a', 'k2s',...,'k12s']
        read string from k2a.txt and strip white chars, return the only Chinese chars
    """
    txt_file = f'source/{name}.txt'
    string = load_string(txt_file)
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

def write_database_order(chars, name):
    """
        write to json file, keep original order
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

    # print(chars)
    print(f'There are {len(chars)} chars in total')

    unique_chars = ''
    for char in chars:
        if not char in unique_chars:
            unique_chars += char
    print(f'There are {len(unique_chars)} unique chars in total')
    print(unique_chars)      
    out_dir = '../p2h_data'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    out_file = os.path.join(out_dir, f'{name}.json')
    chars_statics = {
        name: {
            'quantity': len(unique_chars),
            'chars': unique_chars
        }
    }
    with open(out_file, 'w', encoding='utf-8') as writer:
        json.dump(chars_statics, writer, indent=4, ensure_ascii=False)    

def dump_json(_dict, out_file):
    with open(out_file, 'w', encoding='utf-8') as writer:
        json.dump(_dict, writer, indent=4, ensure_ascii=False)     

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
    k12 = []
    for num in range(1, 7):
        autumn = f'k{num}a'
        spring = f'k{num}s'
        k12.append(autumn)
        k12.append(spring)
    print(k12)
    # k12 = ['k1a', 'k1s', 'k2a']
    chars_k12 = {}
    for name in k12:
        chars = str_k12(name=name)
        write_database_order(chars=chars, name=name)
        chars_k12[name] = {
            'quantity': len(chars),
            'chars': chars
        }

    for num in range(1, 7):
        autumn = f'k{num}a'
        spring = f'k{num}s'
        chars_k_num = chars_k12[autumn]['chars'] + chars_k12[spring]['chars']
        k_num = f'k{num}'
        write_database_order(chars=chars_k_num, name=k_num)
        covered, uncovered, chars_over = relation(chars_k12[autumn]['chars'], chars_k12[spring]['chars'])
        print(f'covered: {covered}')

        chars_k12[k_num] = {
            'quantity': len(chars_k_num),
            'chars': chars_k_num
            }
    out_dir = '../p2h_data'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    out_file = os.path.join(out_dir, f'k12.json')    
    dump_json(_dict = chars_k12, out_file=out_file)

def main():
    # strip_str()
    test1()

if __name__ == "__main__":
    main()