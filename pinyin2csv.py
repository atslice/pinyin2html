import os
from pypinyin import pinyin, Style
from pinyin2html import Pinyin2h

class Pinyin2csv():
    def __init__(self) -> None:
        pass

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
        with open(out_file_chars, 'w') as writer:
            writer.write(csv_chars)
        out_file_chars_gb2312 = os.path.join(out_dir, f'{name}_chars_gb2312.csv')
        with open(out_file_chars_gb2312, 'w', encoding='gb2312') as writer:
            writer.write(csv_chars)            
        out_file_pinyin = os.path.join(out_dir, f'{name}_pinyin.csv')            
        with open(out_file_pinyin, 'w') as writer:
            writer.write(csv_marks)
        out_file_pinyin_r = os.path.join(out_dir, f'{name}_pinyin_r.csv')            
        with open(out_file_pinyin_r, 'w') as writer:
            writer.write(csv_marks_r)
        out_file_pinyin_r_gb2312 = os.path.join(out_dir, f'{name}_pinyin_r_gb2312.csv')            
        with open(out_file_pinyin_r_gb2312, 'w', encoding='gb2312') as writer:
            writer.write(csv_marks_r)            
        print(out_file_pinyin_r)

        # heteronym as reference
        csv_marks, csv_marks_r = self.gen_heteronym_csv(chars=chars, number=number)
        out_file_pinyin = os.path.join(out_dir, f'{name}_pinyin_heteronym.csv')            
        with open(out_file_pinyin, 'w') as writer:
            writer.write(csv_marks)
        out_file_pinyin_r = os.path.join(out_dir, f'{name}_pinyin_heteronym_r.csv')            
        with open(out_file_pinyin_r, 'w') as writer:
            writer.write(csv_marks_r)
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
    p2h = Pinyin2h()
    cnchar = '一个人'
    mark = pinyin(cnchar, heteronym=True)  # heteronym=True 启用多音字模式
    # 多音字模式: '一' -> [['yī', 'yí', 'yì']]
    # heteronym=False  ‘一' -> [['yī']]
    print(mark)  # 即使启用多音字模式, '一个人' -> [['yí'], ['gè'], ['rén']]
    print(type(mark))
    span = p2h.gen_span(char = '你', mark =  mark[0][0])
    print(span)


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

def main():
    chars = '隔江犹唱后庭花回乡偶书其一贺知章离别家乡岁月多近来人事半消磨惟有门前镜湖水春风不改旧时波回乡偶书其二贺知章少小离家老大回乡音无改鬓毛衰儿童相'
    chars = '见不相识笑问客从何处来黄鹤楼送孟浩然之广陵故人西辞黄鹤楼烟花三月下扬州孤帆远影碧空尽唯见长江天际流李白暮江吟白居易一道残阳铺水中半江瑟瑟半江'
    name = chars[-7:]
    str2csv(chars=chars, number=10, name = name)

if __name__ =="__main__":
    main()