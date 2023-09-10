import os

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def format_txt():
    strings = ''
    with open('../data_p2h/k2a.txt', 'r') as reader:
        strings = reader.readlines()
    # print(string)
    
    with open('../data_p2h/out.txt', 'w') as writer:
        for string in strings:
            string = string.strip('\r').strip('\n').replace(' ', '').replace('\t', '').strip()
            if string == '':
                continue
            writer.write(f'{string}\r\n')

def main():
    mkdir('../data_p2h')
    format_txt()

if __name__ == '__main__':
    main()