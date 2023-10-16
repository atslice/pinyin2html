import os
from pypinyin import pinyin, Style

def get_pinyins(chars):
    """
            get pinyins from chars
            Args:
                chars: str, only Chinese chars
            Return: list, the relative pinyin of chars, if some char in chars is not Chinese chars, space or biaodian->empty string
    """

    def is_not_cnchar(char):
        """return boolean"""
        non_chars = '，。[] '
        return True if char in non_chars else False

    def group(chars):
        """
            group non-Chinse chars
            Return: list
        """
        tmp = []
        groups = []
        pre_non = False  # the previous char is non-Chinese char
        for char in chars:
            if is_not_cnchar(char):
                tmp.append(char)
                pre_non = True
            else:
                if pre_non:
                    groups.append(tmp)
                groups.append([char])
                pre_non = False
                tmp = []
        if pre_non:
            groups.append(tmp)  # 当最后一个或几个为非汉字时
        print(groups)
        return groups
    
    def get(chars, groups):
        """
            get pinyins from chars
            Args:
                chars: str, only Chinese chars
            Return: list, the relative pinyin of chars, if some char in chars is not Chinese chars, space->space, biaodian->empty string
        """
        pinyins = []  # 存储对应的拼音, 长度与chars对应，可存储，为方便以后拼音修改
        # marks = pinyin(chars, heteronym=True)
        marks = pinyin(chars)  # list of list, 非多音字模式。如果chars里有连续空格的话，返回的列表长度与chars长度不一致。 TO-DO: 找出多音字，并作出提示
        # print(f'chars: {len(chars)}, marks: {len(marks)}')
        # print(marks)
        # 商歌三首  其一
        # [['shāng'], ['gē'], ['sān'], ['shǒu'], ['  '], ['qí'], ['yī']]
        # 连续空格，则只返回对应空格, 多个空格合并为一个字符串放到一个列表里。如"商歌三首"后是两个空格，但只返回['  ']
        j = 0
        for group in groups:
            # print(j)
            pys = [ '' if is_not_cnchar(char) else marks[j][0]  # 因分词不当，可能有多个读音的情况下，取第一个读音
                    for char in group
                ]
            pinyins += pys
            j += 1
        return pinyins

    groups = group(chars)
    pinyins = get(chars, groups)
    return pinyins

def test_heteronym():
    # 多音字模式, 同一个字返回的拼音结果，因分词不同而不同
    cnchar = '一个人'
    mark = pinyin(cnchar, heteronym=True)  # heteronym=True 启用多音字模式
    # 多音字模式: '一' -> [['yī', 'yí', 'yì']]
    # heteronym=False  ‘一' -> [['yī']]
    print(mark)  # 即使启用多音字模式, '一个人' -> [['yí'], ['gè'], ['rén']]
    print(type(mark))

    cnchar = '孟浩然'
    mark = pinyin(cnchar, heteronym=True)  # heteronym=True 启用多音字模式  
    print(mark)  # [['mèng'], ['hào', 'gǎo', 'gé'], ['rán']]

    cnchar = '好事多磨'
    mark = pinyin(cnchar, heteronym=True)  # heteronym=True 启用多音字模式  
    print(mark)  # [['hǎo'], ['shì'], ['duō'], ['mó']]


    cnchar = '叶公好龙'
    mark = pinyin(cnchar, heteronym=True)  # heteronym=True 启用多音字模式  
    print(mark)  # [['yè'], ['gōng'], ['hào'], ['lóng']]

    cnchar = '好浩好不'
    mark = pinyin(cnchar, heteronym=True)  # heteronym=True 启用多音字模式  
    print(mark)  # [['hǎo', 'hào'], ['hào', 'gǎo', 'gé'], ['hǎo'], ['bù']]
  
    cnchar = '好浩S好pK不'
    mark = pinyin(cnchar, heteronym=True)  # heteronym=True 启用多音字模式  
    print(mark)  # [['hǎo', 'hào'], ['hào', 'gǎo', 'gé'], ['S'], ['hǎo', 'hào'], ['pK'], ['bù', 'fǒu', 'fōu', 'fū', 'bú']]


def test_symbol(chars):
    # chars = '[唐] 孟浩然'
    mark = pinyin(chars, heteronym=True)  # heteronym=True 启用多音字模式
    print(mark)  # [['['], ['táng'], ['] '], ['mèng'], ['hào', 'gǎo', 'gé'], ['rán']]
    # 注意]和空格合并到一个列表里返回了
    # print(type(mark))

    pinyins = get_pinyins(chars=chars)
    print(f'chars length: {len(chars)}, pinyins length: {len(pinyins)}')
    print(pinyins)
    # print(zip(chars, pinyins))


def main():
    # test()
    chars = '[唐] 孟浩然'
    test_symbol(chars)
    chars = '春眠不覺曉，'
    test_symbol(chars)

if __name__ =="__main__":
    main()