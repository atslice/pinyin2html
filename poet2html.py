import os
import copy
from pypinyin import pinyin, Style
from pinyinlib import get_pinyins
from pyjsonlib import  load_json, dump_json
from pyiolib import makedirs, dump_str

class PoetPinyin2h():
    def __init__(self) -> None:
        self.__html_t__ = ''  # 繁体版手机版
        self.__html_s__ = ''  # 简体版手机版
        self.__html_cts__ = ''  # 繁简双排对照打印版
        self.__heteronym__ = {}  # 存储多音字，以诗词标题为key
        self.__poets_pinyin__ = []  # copy of deepcopy incoming poets, but add pinyin data
        self.final = False
        self.poet_title = ''

    def init_for_phone(self):
        self.kaiti_style = f'style="font-family: 楷体, 楷体_gb2312, &quot;Kaiti SC&quot;, STKaiti, &quot;AR PL UKai CN&quot;, &quot;AR PL UKai HK&quot;, &quot;AR PL UKai TW&quot;, &quot;AR PL UKai TW MBE&quot;, &quot;AR PL KaitiM GB&quot;, KaiTi, KaiTi_GB2312, DFKai-SB, TW-Kai, web-fz;"'
        # "text-align:center"
        h_font_size = '50px'
        self.style_headline = f'style="font-size:{h_font_size}; text-align:center"'  # 标题的字体大小

        p_font_size = '50px'
        self.style_paragrah = f'style="font-size:{p_font_size}; text-align:center"'

        p_font_size_author = '40px'
        self.style_paragrah_author = f'style="font-size:{p_font_size_author}; text-align:center"'   # 作者段落的字体应设置比内容段落的字体稍小一点 

        self.style_after_page = 'style="page-break-before: always;"'
        # page_head_height = '116px'  #  116px is the default value
        page_head_height = '116px'
        self.style_page_head = f'style="height: {page_head_height}; line-height: 136px; font-size: 32px; text-align: center; display: none;"'
        # self.style_page_head = f'style="height: {page_head_height}; line-height: 136px; font-size: 32px; text-align: center;"'
        self.div_page_head = f'<div {self.style_page_head}></div>'
        self.div_after_page = f'\n<div {self.style_after_page}>{self.div_page_head}</div>'   # page break per poet

    def init_for_pc(self):
        self.kaiti_style = f'style="font-family: 楷体, 楷体_gb2312, &quot;Kaiti SC&quot;, STKaiti, &quot;AR PL UKai CN&quot;, &quot;AR PL UKai HK&quot;, &quot;AR PL UKai TW&quot;, &quot;AR PL UKai TW MBE&quot;, &quot;AR PL KaitiM GB&quot;, KaiTi, KaiTi_GB2312, DFKai-SB, TW-Kai, web-fz;"'
        # "text-align:center"
        h_font_size = '25px'
        self.style_headline = f'style="font-size:{h_font_size}; text-align:center"'  # 标题的字体大小

        p_font_size = '25px'
        self.style_paragrah = f'style="font-size:{p_font_size}; text-align:center"'

        p_font_size_author = '20px'
        self.style_paragrah_author = f'style="font-size:{p_font_size_author}; text-align:center"'   # 作者段落的字体应设置比内容段落的字体稍小一点 

        self.style_after_page = 'style="page-break-before: always;"'
        # page_head_height = '116px'  #  116px is the default value
        page_head_height = '116px'
        self.style_page_head = f'style="height: {page_head_height}; line-height: 136px; font-size: 32px; text-align: center; display: none;"'
        # self.style_page_head = f'style="height: {page_head_height}; line-height: 136px; font-size: 32px; text-align: center;"'
        self.div_page_head = f'<div {self.style_page_head}></div>'
        self.div_after_page = f'\n<div {self.style_after_page}>{self.div_page_head}</div>'   # page break per poet

    @property
    def heteronym(self):
        """
            多音字列表字典
        """
        return self.__heteronym__

    @property
    def html_t(self):
        """html 标记文本"""
        return self.__html_t__

    @property
    def html_s(self):
        """html 标记文本"""
        return self.__html_s__

    @property
    def html_cts(self):
        """html 标记文本"""
        return self.__html_cts__
    
    @property
    def poets_pinyin(self):
        """return the pinyin-data-added poets list"""
        return self.__poets_pinyin__
       
    def gen_poets_html(self, poets: list, final = False):
        """
            Args:
                poets: list of dict
                final: boolean, if True, it means each poet in poets contains the pinyin data, it is safe to read pinyin data from poets, and should not call pinyin lib to generate pinyin data
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
        self.final = final
        self.__poets_pinyin__ = copy.deepcopy(poets)
        html_start = self.gen_start()
        html_end = self.gen_end()

        # gen Traditional Chinese Edition
        html_t = self.gen_poets_html_t(poets)       
        self.__html_t__  = f'{html_start}{html_t}{html_end}'

        # gen Simplified Chinese Edition
        html_s = self.gen_poets_html_s(poets)       
        self.__html_s__  = f'{html_start}{html_s}{html_end}'

        # gen Traditional vs Simplified Chinese Edition
        html_cts = self.gen_poets_html_cts(poets)       
        self.__html_cts__  = f'{html_start}{html_cts}{html_end}'

        # gen Simplified vs Simplified Chinese Edition       

    def get_poet_length(self, poet):
        """统计当前诗有多少行"""
        return len(poet['paragraphs_break'])

    def gen_poets_html_cts(self, poets):
        """gen Traditional Chinese Edition"""
        poets_html = ''
        self.init_for_pc()

        def add_page_break(str):
            str += self.div_after_page
            return str

        poets_html = add_page_break(poets_html)  # the page head div for the first page, to be the same with the other pages
        cache = True  # cache 为True, 则暂不分页
        for poet in poets:
            length = self.get_poet_length(poet)   # 为节约纸张，如果接连两首诗都是四行，则合并在一页
            if length >= 5 and (not cache):  # 
                poets_html = add_page_break(poets_html)                                
            poet_html_t, poet_pinyins = self.gen_poet_html(poet, edition='t')
            poet_html_s, poet_pinyins = self.gen_poet_html(poet, edition='s')
            div_horizonal= f'\n  <div style="display: flex; justify-content: space-around">{poet_html_t}{poet_html_s}\n  </div>\n'        
            poets_html += div_horizonal
            if length >= 5:
                poets_html = add_page_break(poets_html)
                cache = True  # 设置下一首诗为cache
            else:
                if cache:               
                    # insert blank height
                    div_height = '\n<div style="height: 80px"></div>\n'
                    poets_html += div_height
                    cache = False
                    continue
                else:
                    poets_html = add_page_break(poets_html)
                    cache = True  # 设置下一首诗为cache   
        return poets_html 

    def gen_poets_html_cts2(self, poets):
        """gen Traditional Chinese Edition 不论行数, 逢2分页, 适用于所有诗中，任何连续奇偶两首都可打印在一张纸上"""
        poets_html = ''
        self.init_for_pc()

        def add_page_break(str):
            str += self.div_after_page
            return str

        poets_html = add_page_break(poets_html)  # the page head div for the first page, to be the same with the other pages
        i = 0
        for poet in poets:
            i += 1                               
            poet_html_t, poet_pinyins = self.gen_poet_html(poet, edition='t')
            poet_html_s, poet_pinyins = self.gen_poet_html(poet, edition='s')
            div_horizonal= f'\n  <div style="display: flex; justify-content: space-around">{poet_html_t}{poet_html_s}\n  </div>\n'        
            poets_html += div_horizonal
            if (i % 2) == 0:
                poets_html = add_page_break(poets_html)
            else:
                div_height = '\n<div style="height: 60px"></div>\n'
                poets_html += div_height  
        return poets_html 

    def gen_poets_html_t(self, poets):
        """gen Traditional Chinese Edition"""
        poets_html = ''
        self.init_for_phone()
        poets_html += self.div_page_head  # the page head div for the first page, to be the same with the other pages
        i = 0  # 为方便update self.__poets_pinyin__
        for poet in poets:
            poet_html, poet_pinyins = self.gen_poet_html(poet, edition='t')
            poet_html += self.div_after_page
            poets_html += poet_html
            if not self.final:
                self.__poets_pinyin__[i].update(poet_pinyins)
            i += 1
        return poets_html       

    def gen_poets_html_s(self, poets):
        """gen Simplified Chinese Edition"""
        poets_html = ''
        self.init_for_phone()
        poets_html += self.div_page_head  # the page head div for the first page, to be the same with the other pages
        i = 0  # 为方便update self.__poets_pinyin__
        for poet in poets:
            poet_html, poet_pinyins = self.gen_poet_html(poet, edition='s')
            poet_html += self.div_after_page
            poets_html += poet_html
            if not self.final:
                self.__poets_pinyin__[i].update(poet_pinyins)
            i += 1
        return poets_html 

    def gen_poet_html(self, poet, edition = 't'):
        """
            Args:
                poet: dict
                edition: str, available values:
                    't': Traditional Chinese Edition
                    's': Simplified Chinese Edition
                    'c': Traditional vs Simplified Chinese Edition
            Return: (str, dict)
                str: html str
                dict: pinyin data of the poet
        """
        html_str = ''           
        if edition == 't':
            title_key = 'title'
            title = poet[title_key]
            self.poet_title = f'{title}_繁体版'  # 为多音字列表而准备
            time_key = 'time'
            author_key = 'author'
            time_author_key = 'time_author'
            time_author = poet[time_author_key]
            paragraphs_key = 'paragraphs_break'  # one sentence each line         
        elif edition == 's':
            title_key = 'title_simple'
            title = poet[title_key]
            self.poet_title = f'{title}_简体版'  # 为多音字列表而准备
            time_key = 'time_simple'
            author_key = 'author_simple'
            time_author_key = 'time_author_simple'
            time_author = poet[time_author_key]
            paragraphs_key = 'paragraphs_break_simple'  # one sentence each line 
        title_pinyins_key = f'{title_key}_pinyins'
        time_author_pinyins_key = f'{time_author_key}_pinyins'
        time_pinyins_key = f'{time_key}_pinyins'
        author_pinyins_key = f'{author_key}_pinyins'
        paragraphs_pinyins_key = f'{paragraphs_key}_pinyins'
        paragraphs = poet[paragraphs_key]

        print(title)
        time_pinyins = self.find_pinyins(poet[time_key])
        author_pinyins = self.find_pinyins(poet[author_key])

        pinyins = poet[title_pinyins_key] if self.final else []
        title_paragraph, title_pinyins = self.gen_headline_html(chars=title, pinyins=pinyins, level=1, style=self.style_headline)

        pinyins = poet[time_author_pinyins_key] if self.final else []
        author_paragraph, time_author_pinyins = self.gen_paragrah_html(chars=time_author, pinyins=pinyins, style=self.style_paragrah_author)

        if self.final:  # each poet contains pinyin data
            paragraphs_pinyins_db = poet[paragraphs_pinyins_key]
        poet_paragraphs = ''
        paragraphs_pinyins = {}  # 存储分行诗句对应的拼音
        for paragraph in paragraphs:
            pinyins = paragraphs_pinyins_db[paragraph] if self.final else []
            poet_paragraph, paragraph_pinyins = self.gen_paragrah_html(chars=paragraph, pinyins=pinyins, style=self.style_paragrah)
            poet_paragraphs += poet_paragraph
            paragraphs_pinyins[paragraph] = paragraph_pinyins
        html_str = f'{title_paragraph}{author_paragraph}{poet_paragraphs}'
        poet_pinyins = {
                title_pinyins_key: title_pinyins,
                time_pinyins_key: time_pinyins,
                author_pinyins_key: author_pinyins,                
                time_author_pinyins_key: time_author_pinyins,
                paragraphs_pinyins_key: paragraphs_pinyins
            }
        html_str = f'\n    <div class="poet">{html_str}\n    </div>\n'
        return html_str, poet_pinyins

    def gen_headline_html(self, chars, pinyins, level = 1, style = ''):
        """
            generate html headline with pinyin han span
            Args:
                chars: str, only Chinese chars
                pinyins: list of str, the pinyin data relative with chars, usefull when final pinyin data is already in poet
                level: int, from 1 to 6
                style: str, the leagal style attribute
        """
        if not level in (1, 2, 3, 4, 5, 6):
            raise ValueError('level must be int range from 1 to 6')
        tag_start = f'\n      <h{level} {style}>'
        tag_end = f'\n      </h{level}>'
        if self.final:
            spans, pinyins2 = self.gen_pinyin_han_final(chars, pinyins)
        else:
            spans, pinyins2 = self.gen_pinyin_han(chars)
        return f'{tag_start}{spans}{tag_end}', pinyins2

    def gen_paragrah_html(self, chars, pinyins, style = ''):
        """
            generate html paragrah with pinyin han span
            Args:
                chars: str, only Chinese chars
                pinyins: list of str, the pinyin data relative with chars, usefull when final pinyin data is already in poet
                style: str, the leagal style attribute of font-size, text-align, etc
        """     
        tag_start = f'\n      <p {style}>'
        tag_end = '\n      </p>'
        if self.final:
            spans, pinyins2 = self.gen_pinyin_han_final(chars, pinyins)
        else:
            spans, pinyins2 = self.gen_pinyin_han(chars)
        return f'{tag_start}{spans}{tag_end}', pinyins2

    def get_heteronym_list(self, chars):
        """
            Return: 多音字字典列表
        """
        if not self.poet_title in self.__heteronym__:
            self.__heteronym__[self.poet_title] = {}
        for char in chars:
            marks = pinyin(char, heteronym=True)  # '落' -> [['luò', 'là', 'lào', 'luō']];  '。' -> [['。']]
            print(f'{char}: {len(marks[0])} {marks[0]}')
            if len(marks[0]) > 1:  # 有多个读音
                self.__heteronym__[self.poet_title].update({
                    char: marks[0]
                })

    def find_pinyins(self, chars):
        """
            get pinyins from chars
            Args:
                chars: str, only Chinese chars
            Return: list, the relative pinyin of chars, if some char in chars is not Chinese chars, space biaodian->empty string
        """
        pinyins = get_pinyins(chars)     
        return pinyins

    def gen_pinyin_han(self, chars):
        """
            generate html pinyin han span
            Args:
                chars: str, only Chinese chars
            Return: (str, list)
                str: html spans
                list: the relative pinyin of chars, if some char in chars is not Chinese chars, space->space, biaodian->empty string
        """
        print(f'len = {len(chars)}, chars = {chars}')
        pinyins = self.find_pinyins(chars)
        print(f'len = {len(pinyins)}, pinyins = {pinyins}')
        spans, _ = self.gen_pinyin_han_final(chars, pinyins)
        return spans, pinyins

    def gen_pinyin_han_final(self, chars, pinyins):
        """
            generate html pinyin han span
            Args:
                chars: str, only Chinese chars
                pinyins: list of str, the pinyin data relative with chars, usefull when final pinyin data is already in poet
            Return: (str, list)
                str: html spans
                list: the relative pinyin of chars, the same as argument pinyins
        """
        self.get_heteronym_list(chars)  # 虽然不用pinyin lib来查找拼音，仍然列出多音字 
        spans = ''
        i = 0  # for easy reading data in pinyins
        for char in chars:
            print(f'{char} {i} {pinyins[i]}')
            mark = pinyins[i]
            span = self.gen_span(char=char, mark=mark)
            i += 1      
            spans = f'{spans}{span}'
        spans = f'{spans}'
        return spans, pinyins

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
        # style="text-align:center"
        html_start = """
<html>

<body>       
        """
        return html_start
    
    def gen_end(self):
        html_end = """
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


def poets2html(out_dir, name, poets, final=False):
    """
        Args:
            out_dir: str, the path to store to result files
            name: str, the basename of file without extension
            poets: list of dict
            final: boolean, if True, it means each poet in poets contains the pinyin data, it is safe to read pinyin data from poets, and should not call pinyin lib to generate pinyin data            
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
    p2h = PoetPinyin2h()
    p2h.gen_poets_html(poets=poets, final=final)

    out_file = os.path.join(out_dir, f'{name}_繁体版.html')
    dump_str(_file=out_file, _str=p2h.html_t)

    out_file = os.path.join(out_dir, f'{name}_简体版.html')
    dump_str(_file=out_file, _str=p2h.html_s)

    out_file = os.path.join(out_dir, f'{name}_繁简对照打印版.html')
    dump_str(_file=out_file, _str=p2h.html_cts)  

    heteronym_json = os.path.join(out_dir, f'{name}_heteronym.json')
    dump_json(_file=heteronym_json, _dict=p2h.heteronym)

    poets_pinyin_json = os.path.join(out_dir, f'{name}_pinyin.json')
    dump_json(_file=poets_pinyin_json, _dict=p2h.poets_pinyin)

    print(out_file)    

def json2html(out_dir, input_json, name, final=False):
    """
        final: boolean, if True, it means each poet in poets contains the pinyin data, it is safe to read pinyin data from poets, and should not call pinyin lib to generate pinyin data                
    """
    poets = load_json(input_json) # list
    poets2html(out_dir, name, poets, final)

def main():
    out_dir = '../p2h_data'
    makedirs(out_dir)    
    name = '古诗接龙_break_simple_add_pinyin'
    input_json = f'input/final/{name}.json'
    json2html(out_dir, input_json, name, final=True)    


if __name__ =="__main__":
    main()