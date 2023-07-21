import os
from pypinyin import pinyin, Style

class Pinyin2h():
    def __init__(self) -> None:
        pass

    def dump_html(self, chars: str, number: int, out_file = None):
        """
            Args:
                number: limit the number of chars in a line
        """        
        if out_file is None:
            return
        with open(out_file, 'w') as writer:
            writer.write(self.gen_html(chars=chars, number=number))

    def gen_html(self, chars: str, number: int):
        """
            Args:
                number: limit the number of chars in a line
        """
        html_str = ''
        html_start = self.gen_start()
        html_end = self.gen_end()
        # marks = pinyin(chars, heteronym=True)
        marks = pinyin(chars)
        i, j = 0, 0
        paragraphs = ''
        paragraph = ''
        p_start = '<p>'
        p_end = '</p>'
        p_open = False
        for char in chars:
            span = self.gen_span(char=char, mark=marks[i][0])
            i += 1           
            paragraph = f'{paragraph}{span}'
            if j == 0:
                paragraph = f'{p_start}{paragraph}'
                p_open = True
                print(f'{i} {j}: p_open')
            elif j == number - 1:
                paragraph = f'{paragraph}{p_end}'
                paragraphs = f'{paragraphs}{paragraph}'
                p_open = False
                print(f'{i} {j}: p_close')
                j = -1
            j += 1
        if p_open:
            paragraphs = f'{paragraphs}{p_end}'
            print(f'{i} {j}: The final p_close')

        html_str = f'{html_start}{paragraph}{html_end}'
        return html_str

    def gen_html_heteronym(self, chars: str):
        html_str = self.gen_start()
        for char in chars:
            mark = pinyin(char, heteronym=True)
            span = self.gen_span(char=char, mark=mark)
            html_str = f'{html_str}{span}'
        html_end = self.gen_end()
        html_str = f'{html_str}{html_end}'
        return html_str

    def gen_start(self):
        html_start = """
<html>

<body>
    <div style="text-align:center">        
        """
        return html_start
    
    def gen_end(self):
        html_end = """
    </div>
</body>

</html>      
        """
        return html_end   

    def gen_span(self, char: str, mark: str):
        module = """
        <span class="py-result-item">
            <ruby>
                <span class="py-chinese-item">{汉}</span>
                <rp>(</rp>
                <rt class="py-pinyin-item">{hàn}</rt>
                <rp>)</rp>
            </ruby>
        </span>        
        """
        return module.format_map({'汉': char, 'hàn': mark})

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

def str2html(chars: str, number: int):
    """
            Args:
                number: limit the number of chars in a line
    """    
    p2h = Pinyin2h()
    # chars = '春眠不觉'
    out_dir = '../p2h_data'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    out_file = os.path.join(out_dir, f'{chars[:20]}.html')
    # html = p2h.gen_html(chars=chars)
    # print(html)
    p2h.dump_html(chars=chars, number = number, out_file=out_file)
    print(out_file)

def main():
    from database_gen import str_k1a
    chars = str_k1a()
    str2html(chars=chars, number=12)

if __name__ =="__main__":
    main()