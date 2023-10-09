import json
import datetime

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):  # consider to judge tzinfo
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def dump_json_sort(_file, _dict):
    with open(_file, 'w') as fp:
        json.dump(_dict, fp, cls = ComplexEncoder, indent=4, sort_keys=True, ensure_ascii=False)

def dump_json(_file, _dict):
    with open(_file, 'w') as fp:
        json.dump(_dict, fp, cls = ComplexEncoder, indent=4, sort_keys=False, ensure_ascii=False)

def dump_json_sort_ascii(_file, _dict):
    with open(_file, 'w') as fp:
        json.dump(_dict, fp, cls = ComplexEncoder, indent=4, sort_keys=True)

def load_json(_file):
    with open(_file, 'r') as reader:
        return json.load(reader)

def beautify(in_file, out_file):
    import codecs
    with codecs.open(in_file, 'rb') as fp:
        in_json = json.load(fp)
    with codecs.open(out_file, 'w') as fp:
        json.dump(in_json, fp, indent=4, sort_keys=True)

def parse_args():
    """
        parse arguments
        return: the first argv str if there are any passed arguments; None if no argument is passed
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in-file", type=str, help="input json file")
    parser.add_argument("-o", "--out-file", type=str, help="output json file")
    args = parser.parse_args()
    return args
        
def main():
    args = parse_args()
    in_file = args.in_file
    out_file = args.out_file
    beautify(in_file, out_file)
    print(out_file)

if __name__ == "__main__":
    main()
