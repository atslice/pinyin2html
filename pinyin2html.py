import re
from pypinyin import pinyin, Style

class Pinyin2h():
    def __init__(self) -> None:
        pass

    def gen_start(self):
        html_start = """
<html>

<body>
    <div>        
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

def main():
    p2h = Pinyin2h()
    cnchar = '一个人'
    mark = pinyin(cnchar, heteronym=True)  # heteronym=True 启用多音字模式
    # 多音字模式: '一' -> [['yī', 'yí', 'yì']]
    # heteronym=False  ‘一' -> [['yī']]
    print(mark)  # 即使启用多音字模式, '一个人' -> [['yí'], ['gè'], ['rén']]
    print(type(mark))
    span = p2h.gen_span(char = '你', mark =  mark[0][0])
    print(span)

if __name__ =="__main__":
    main()