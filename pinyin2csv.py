import os
from pypinyin import pinyin, Style
from pinyin2html import Pinyin2h

class Pinyin2csv():
    def __init__(self) -> None:
        pass

    def dump_html(self, chars: str, number: int, out_file = None, out_file_pinyin = None):
        """
            Args:
                number: limit the number of chars in a line
        """        
        if out_file is None:
            return
        csv_chars, csv_marks = self.gen_csv(chars=chars, number=number)
        with open(out_file, 'w') as writer:
            writer.write(csv_chars)
        with open(out_file_pinyin, 'w') as writer:
            writer.write(csv_marks)            

    def gen_csv(self, chars: str, number: int):
        """
            Args:
                number: limit the number of chars in a line
            Return: (str, str)
        """
        # marks = pinyin(chars, heteronym=True)
        marks = pinyin(chars)  # return list of list
        i, j = 0, 0  # i counts the order of chars, j counts the order of a char in a line
        csv_chars = ''
        csv_line = ''
        csv_marks = ''
        csv_mark_line = ''
        p_open = True
        for char in chars:
            mark=marks[i][0]
            i += 1           
            if j == 0:  # the beginning of a line
                csv_line = ''
                csv_mark_line = ''
            csv_line = f'{csv_line}{char}'
            csv_mark_line = f'{csv_mark_line}{mark}'                
            if j < number - 1:
                csv_line = f'{csv_line},'
                csv_mark_line = f'{csv_mark_line},'                
            elif j == number - 1:  # the last char in a line
                p_open = False
                csv_line = f'{csv_line}\r\n'
                csv_chars = f'{csv_chars}{csv_line}'
                csv_mark_line = f'{csv_mark_line}\r\n'                
                csv_marks = f'{csv_marks}{csv_mark_line}'
                print(f'{i} {j}: p_close')
                j = -1
            j += 1
        if p_open:
            csv_chars = f'{csv_chars}{csv_line}'
            csv_marks = f'{csv_marks}{csv_mark_line}'
        return csv_chars, csv_marks



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


def str2csv(chars: str, number: int):
    """
            Args:
                number: limit the number of chars in a line
    """    
    p2h = Pinyin2csv()
    # chars = '春眠不觉'
    out_dir = '../p2h_data'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    out_file = os.path.join(out_dir, f'{chars[:20]}.csv')
    out_file_pinyin = os.path.join(out_dir, f'{chars[:20]}_pinyin.csv')    
    p2h.dump_html(chars=chars, number = number, out_file=out_file, out_file_pinyin = out_file_pinyin)
    print(out_file)

def main():
    chars = '隔江犹唱后庭花回乡偶书其一贺知章离别家乡岁月多近来人事半消磨'
    str2csv(chars=chars, number=10)

if __name__ =="__main__":
    main()