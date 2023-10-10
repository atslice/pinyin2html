import os
from pypinyin import pinyin, Style
from pyjsonlib import  load_json, dump_json
from pyiolib import makedirs

class Pinyin2h():
    def __init__(self) -> None:
        self.kaiti_style = """
style="font-family: 楷体, 楷体_gb2312, &quot;Kaiti SC&quot;, STKaiti, &quot;AR PL UKai CN&quot;, &quot;AR PL UKai HK&quot;, &quot;AR PL UKai TW&quot;, &quot;AR PL UKai TW MBE&quot;, &quot;AR PL KaitiM GB&quot;, KaiTi, KaiTi_GB2312, DFKai-SB, TW-Kai, web-fz;"        
        """
        self.style_after_page = 'style="page-break-before: always;"'
        self.style_page_head = 'style="height: 116px; line-height: 136px; font-size: 32px; text-align: center; display: none;"'
        self.div_page_head = f'<div {self.style_page_head}></div>'
        self.div_after_page = f'\n<div {self.style_after_page}>{self.div_page_head}</div>'   # page break per poet

    def dump_html(self, chars: str, number: int, out_file = None):
        """
            Args:
                number: limit the number of chars in a line
        """        
        if out_file is None:
            return
        with open(out_file, 'w') as writer:
            writer.write(self.gen_html(chars=chars, number=number))

    def dump_poets_html(self, poets: list, out_file = None):
        """
            Args:
            poets: list of dict
        Example:
    [   {
        "author": "孟浩然",
        "paragraphs": [
            "春眠不覺曉，處處聞啼鳥。",
            "夜來風雨聲，花落知多少。"
        ],
        "tags": [
            "唐诗三百首",
            "春",
            "写景",
            "一年级下册",
            "惜春",
            "五言绝句",
            "小学古诗"
        ],
        "title": "春曉",
        "id": "cb168b3b-d104-4df7-9868-1e1225ddb941"
        },
    ]
        """        
        if out_file is None:
            return
        with open(out_file, 'w') as writer:
            writer.write(self.gen_poets_html(poets))

    def gen_poets_html(self, poets):
        """
            Args:
                poets: list of dict
        """
        html_str = ''
        html_start = self.gen_start()
        html_end = self.gen_end()
        poets_html = ''
        for poet in poets:
            poet_html = self.gen_poet_html(poet)
            poet_html += self.div_after_page
            poets_html += poet_html
        html_str = f'{html_start}{poets_html}{html_end}'
        return html_str

    def gen_poet_html(self, poet):
        """
            Args:
                poet: dict
        """
        html_str = ''
        title = poet['title']
        author = poet['author']
        paragraphs = poet['paragraphs']

        print(title)
        title_paragraph = self.gen_paragrah_html(chars=title)
        author_paragraph = self.gen_paragrah_html(chars=author)
        poet_paragraphs = ''
        for paragraph in paragraphs:
            poet_paragraph = self.gen_paragrah_html(chars=paragraph)  # TODO 需要处理标点符号
            poet_paragraphs += poet_paragraph
        html_str = f'{title_paragraph}{author_paragraph}{poet_paragraphs}'
        return html_str

    def gen_paragrah_html(self, chars):
        """
            generate html paragrah with pinyin span
            Args:
                chars: str, only Chinese chars
        """
        def get_mark(i, marks):
            """
                Args:
                    i: int
                    marks: list
                Return: (int, str)
                取到非空拼音为止
            """
            mark = marks[i][0]
            while ' ' in mark:
                i += 1
                mark = marks[i][0]
            return i, mark
            
        paragraph = ''
        # marks = pinyin(chars, heteronym=True)
        marks = pinyin(chars)  # list of list, 非多音字模式。如果chars里有连续空格的话，返回的列表长度与chars长度不一致。 TO-DO: 找出多音字，并作出提示
        # print(f'chars: {len(chars)}, marks: {len(marks)}')
        # print(marks)
        # 商歌三首  其一
        # [['shāng'], ['gē'], ['sān'], ['shǒu'], ['  '], ['qí'], ['yī']]
        # 连续空格，则只返回对应空格, 多个空格合并为一个字符串放到一个列表里
        # if ' ' in chars:
        #    raise ValueError('stop by user')
        p_start = '<p>'
        p_end = '</p>'
        i = 0
        biaodian = '，。'
        for char in chars:
            if char == ' ':  # char是空格，marks里没有对应的空列表，i不自加，否则会导致index越界
                span = self.gen_span(char=' ', mark=' ')
            else:
                i, mark = get_mark(i, marks)  # 取到非空格拼音为止
                mark = '' if char in biaodian else mark   #  标点符号则不注拼音。 下面代码结果同: '' if mark in biaodian else mark
                span = self.gen_span(char=char, mark=mark) #  i 对应汉字字符
                i += 1      
            paragraph = f'{paragraph}{span}'
        paragraph = f'\n{p_start}{paragraph}{p_end}'
        return paragraph

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
                <span class="py-chinese-item" {style}>{汉}</span>
                <rp>(</rp>
                <rt class="py-pinyin-item">{hàn}</rt>
                <rp>)</rp>
            </ruby>
        </span>        
        """
        return module.format_map({'style': self.kaiti_style, '汉': char, 'hàn': mark})

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


def poets2html(out_file, poets):
    """
        Args:
            out_file: str, the path to store to result file
            poets: list of dict
        Example:
    [   {
        "author": "孟浩然",
        "paragraphs": [
            "春眠不覺曉，處處聞啼鳥。",
            "夜來風雨聲，花落知多少。"
        ],
        "tags": [
            "唐诗三百首",
            "春",
            "写景",
            "一年级下册",
            "惜春",
            "五言绝句",
            "小学古诗"
        ],
        "title": "春曉",
        "id": "cb168b3b-d104-4df7-9868-1e1225ddb941"
        },
    ]
    """
    p2h = Pinyin2h()
    p2h.dump_poets_html(poets=poets, out_file=out_file)
    print(out_file)    

def json2html(input_json, name):
    # load input file
    # input_json = 'input/孟浩然_春.json'
    # input_json = 'input/古诗接龙.json'
    poets = load_json(input_json) # list

    out_dir = '../p2h_data'
    makedirs(out_dir)
    out_file = os.path.join(out_dir, f'{name}.html')
    poets2html(out_file, poets)

def main():
    # name = '古诗接龙'
    # input_json = f'input/{name}.json'
    # json2html(input_json, name)

    name = '古诗接龙_simple'
    input_json = f'input/{name}.json'
    json2html(input_json, name)    


if __name__ =="__main__":
    main()