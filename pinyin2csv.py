import os
import json
import codecs
# from pypinyin import pinyin, Style


class Pinyin2csv():
    def __init__(self) -> None:
        pass

    def write_file(self, _file, _str, encoding = None):
        """
            write str to file
        """
        if encoding is None:
            with open(_file, 'w') as writer:
                writer.write(_str)
        else:
            with open(_file, 'w', encoding=encoding) as writer:
                writer.write(_str)                     

    def dump_html(self, chars: str, number: int, out_dir = None, out_name = None):
        """
            Args:
                number: limit the number of chars in a line
        """        
        if out_dir is None:
            return
        name = chars[:10] if out_name is None else out_name

        # default mode
        csv_chars, csv_marks, csv_marks_r = self.gen_csv(chars=chars, number=number)

        out_file_chars = os.path.join(out_dir, f'{name}_chars.csv')
        self.write_file(_file = out_file_chars, _str = csv_chars)

        out_file_chars_gb2312 = os.path.join(out_dir, f'{name}_chars_gb2312.csv')
        self.write_file(_file = out_file_chars_gb2312, _str = csv_chars, encoding='gb2312') 

        out_file_pinyin = os.path.join(out_dir, f'{name}_pinyin.csv')            
        self.write_file(_file = out_file_pinyin, _str = csv_marks)

        out_file_pinyin_gb2312 = os.path.join(out_dir, f'{name}_pinyin_gb2312.csv')            
        self.write_file(_file = out_file_pinyin_gb2312, _str = csv_marks, encoding='gb2312')        

        out_file_pinyin_r = os.path.join(out_dir, f'{name}_pinyin_r.csv')            
        self.write_file(_file = out_file_pinyin_r, _str = csv_marks_r)

        out_file_pinyin_r_gb2312 = os.path.join(out_dir, f'{name}_pinyin_r_gb2312.csv')            
        self.write_file(_file = out_file_pinyin_r_gb2312, _str = csv_marks_r, encoding='gb2312')            
        print(out_file_pinyin_r)

        # heteronym as reference
        csv_marks, csv_marks_r = self.gen_heteronym_csv(chars=chars, number=number)

        out_file_pinyin = os.path.join(out_dir, f'{name}_pinyin_heteronym.csv')            
        self.write_file(_file = out_file_pinyin, _str = csv_marks)

        out_file_pinyin_gb2312 = os.path.join(out_dir, f'{name}_pinyin_heteronym_gb2312.csv')            
        self.write_file(_file = out_file_pinyin_gb2312, _str = csv_marks, encoding='gb2312')        

        out_file_pinyin_r = os.path.join(out_dir, f'{name}_pinyin_heteronym_r.csv')            
        self.write_file(_file = out_file_pinyin_r, _str = csv_marks_r)

        out_file_pinyin_r_gb2312 = os.path.join(out_dir, f'{name}_pinyin_heteronym_r_gb2312.csv')
        self.write_file(_file = out_file_pinyin_r_gb2312, _str = csv_marks_r, encoding='gb2312')           
        print(out_file_pinyin_r)        



    def gen_csv(self, chars: str, number: int):
        """
            Args:
                number: limit the number of chars in a line
            Return: (str, str, str)
        """
        # marks = pinyin(chars, heteronym=True)
        marks = pinyin(chars)  # return list of list
        i, j = 0, 0  # i counts the order of chars, j counts the order of a char in a line
        csv_chars = ''
        csv_line = ''
        csv_marks = ''
        csv_mark_line = ''
        csv_marks_r = ''  # reverse
        csv_mark_line_r = ''        
        p_open = False
        for char in chars:
            mark=marks[i][0]
            # print(i, char, mark)
            i += 1           
            if j == 0:  # the beginning of a line
                p_open = True
                csv_line = ''
                csv_mark_line = ''
                csv_mark_line_r = ''
            csv_line = f'{csv_line}{char}'
            csv_mark_line = f'{csv_mark_line}{mark}'
            csv_mark_line_r = f'{mark}{csv_mark_line_r}'                
            if j < number - 1:
                csv_line = f'{csv_line},'
                csv_mark_line = f'{csv_mark_line},'
                csv_mark_line_r = f',{csv_mark_line_r}'              
            elif j == number - 1:  # the last char in a line
                p_open = False
                csv_line = f'{csv_line}\r\n'
                csv_chars = f'{csv_chars}{csv_line}'
                csv_mark_line = f'{csv_mark_line}\r\n'                
                csv_marks = f'{csv_marks}{csv_mark_line}'
                csv_mark_line_r = f'{csv_mark_line_r}\r\n'               
                csv_marks_r = f'{csv_marks_r}{csv_mark_line_r}'              
                # print(f'{i} {j}: p_close')
                j = -1
            j += 1
        if p_open:
            if j != 0:  # line not full
                for k in range(number - j - 1):
                    print(f'adding , {k}')
                    csv_line = f'{csv_line},'
                    csv_mark_line = f'{csv_mark_line},'
                    csv_mark_line_r = f',{csv_mark_line_r}'
            csv_chars = f'{csv_chars}{csv_line}'
            csv_marks = f'{csv_marks}{csv_mark_line}'
            csv_marks_r = f'{csv_marks_r}{csv_mark_line_r}'            
        return csv_chars, csv_marks, csv_marks_r

    def gen_heteronym_csv(self, chars: str, number: int):
        """
            Args:
                number: limit the number of chars in a line
            Return: (str, str)
        """
        
        i, j = 0, 0  # i counts the order of chars, j counts the order of a char in a line
        csv_marks = ''
        csv_mark_line = ''
        csv_marks_r = ''  # reverse
        csv_mark_line_r = ''        
        p_open = False
        for char in chars:
            marks = pinyin(char, heteronym=True)  # return list of list
            mark=marks[0]  # mark is type of list
            if len(mark) > 1:
                print(i, char, mark)
            i += 1           
            if j == 0:  # the beginning of a line
                p_open = True
                csv_line = ''
                csv_mark_line = ''
                csv_mark_line_r = ''
            csv_mark_line = f'{csv_mark_line}{mark}'
            csv_mark_line_r = f'{mark}{csv_mark_line_r}'                
            if j < number - 1:
                csv_mark_line = f'{csv_mark_line},'
                csv_mark_line_r = f',{csv_mark_line_r}'              
            elif j == number - 1:  # the last char in a line
                p_open = False
                csv_mark_line = f'{csv_mark_line}\r\n'                
                csv_marks = f'{csv_marks}{csv_mark_line}'
                csv_mark_line_r = f'{csv_mark_line_r}\r\n'               
                csv_marks_r = f'{csv_marks_r}{csv_mark_line_r}'              
                # print(f'{i} {j}: p_close')
                j = -1
            j += 1
        if p_open:
            if j != 0:  # line not full
                for k in range(number - j - 1):
                    print(f'adding , {k}')
                    csv_mark_line = f'{csv_mark_line},'
                    csv_mark_line_r = f',{csv_mark_line_r}'
            csv_marks = f'{csv_marks}{csv_mark_line}'
            csv_marks_r = f'{csv_marks_r}{csv_mark_line_r}'            
        return csv_marks, csv_marks_r



def test():
    cnchar = '一个人'
    mark = pinyin(cnchar, heteronym=True)  # heteronym=True 启用多音字模式
    # heteronym=True, 多音字模式: '一' -> [['yī', 'yí', 'yì']]
    # heteronym=True, 即使启用多音字模式, '一个人' -> [['yí'], ['gè'], ['rén']]
    # heteronym=False, 非多音字模式:  ‘一' -> [['yī']]
    print(mark)  # 即使启用多音字模式, '一个人' -> [['yí'], ['gè'], ['rén']]
    print(type(mark))

def str2csv(chars: str, number: int, name: str):
    """
            Args:
                number: limit the number of chars in a line
    """    
    p2h = Pinyin2csv()
    # chars = '春眠不觉'
    out_dir = '../p2h_data'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    print(f'There are {len(chars)} chars to be parsed.') 
    p2h.dump_html(chars=chars, number = number, out_dir=out_dir, out_name = name)

def load_json(_file):
    with open(_file, 'r') as reader:
        return json.load(reader)

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

def unique(_str):
    """
        remove duplicated chars in string, keep original order
        Args:
            _str: str
        Return: str
    """
    new = ''
    for char in _str:
        if not char in new:
            new += char
    return new

def unique_join(strings):
    """
        Args:
            strings: list of str
        Return: str, the joined str in the list, and the duplicated chars are removed
    """

    all_string = ''
    for string in strings:
        all_string += string
    unique_string = unique(all_string)
    print(f'unique_join: unique/total = {len(unique_string)}/{len(all_string)}')
    return unique_string

def statics(string, suffix = '0'):
    """
        write statics about the reloation between the string and the chars in database
        Args:
            string: str, the chars in the str should be unique
            suffix: str, the suffix for the chars_statics.json
    """
    chars_statics = {
        'chars': {
            'chars_num': len(string),
            'chars': string
        }

    }

    db_dir = 'database/people'
    sum_json = f'{db_dir}/sum.json'
    keys = ['k1a', 'k1', 'k1-2', 'k1-3', 'k1-4', 'k1-5', 'k1-6']
    sum = load_json(sum_json)
    for key in  keys:
        chars = sum[key]['chars']  # str, unique chars
        covered, uncovered, over = relation(chars, string)
        chars_statics[key] = {
            'chars_num': len(chars),
            'chars': chars,
            'covered_num': len(covered),
            'covered': covered,
            'uncovered_num': len(uncovered),
            'uncovered': uncovered,
            'over_num': len(over),
            'over': over,
        }

    out_dir = '../p2h_data'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    out_file = os.path.join(out_dir, f'chars_statics_{suffix}.json')

    with codecs.open(out_file, 'w', encoding='utf-8') as writer:
        json.dump(chars_statics, writer, indent=4, ensure_ascii=False)
    print(out_file)
      

    

def main():
    strings = [
        '绝句其三杜甫迟日江山丽春风花草香泥融飞燕子沙暖睡鸳鸯',
        '咏鹅骆宾王鹅鹅鹅曲项向天歌白毛浮绿水红掌拨清波悯农其一其二李绅春种一粒粟秋收万颗子四海无闲田农夫犹饿死锄禾日当午汗滴禾下土谁知盘中餐粒皆辛苦',
        '夜宿山寺李白危楼高百尺手可摘星辰不敢高声语恐惊天上人静夜思床前明月光疑是地上霜举头望明月低头思故乡登鹳雀楼王之涣白日依山尽黄河入海流欲穷千里',
        '目更上一层楼春晓孟浩寻隐者不遇贾岛松下问童子言师采药去只在此山中云深不知处清明杜牧清明时节雨纷纷路上行人欲断魂借问酒家何处有牧童遥指杏花村登',
        '隔江犹唱后庭花回乡偶书其一贺知章离别家乡岁月多近来人事半消磨惟有门前镜湖水春风不改旧时波回乡偶书其二贺知章少小离家老大回乡音无改鬓毛衰儿童相',
        '见不相识笑问客从何处来黄鹤楼送孟浩然之广陵故人西辞黄鹤楼烟花三月下扬州孤帆远影碧空尽唯见长江天际流李白暮江吟白居易一道残阳铺水中半江瑟瑟半江',
        '一日还两岸猿声啼不住轻舟已过万重山寻隐者不遇贾岛松下问童子言师采药去只在此山中云深不知处泊秦淮杜牧烟笼寒水月笼沙夜泊秦淮近酒家商女不知亡国恨'
    ]
    suffix = f'{len(strings)}'
    string = unique_join(strings)
    statics(string, suffix=suffix)
    # return
    chars = strings[-1]
    name = chars[-7:]
    str2csv(chars=chars, number=10, name = name)

if __name__ =="__main__":
    main()