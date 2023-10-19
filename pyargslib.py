import argparse

def parse_args_example():
    """
        parse arguments
        return: the first argv str if there are any passed arguments; None if no argument is passed
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--source", type=str, nargs='+', help="enable the specified source(s) only, can use mutliple -s")  # para nargs='+', form a list for args.source
        parser.add_argument("-md", "--mode", type=str, help="only regen modi file for specified source only")
        parser.add_argument("-m", "--max-titles", type=int, help="limit the max titles")
        parser.add_argument("-l", "--url", action="store_true", help="parse from conf_test/urls.txt")
        args = parser.parse_args()        
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", type=str, nargs='+', help="enable the specified source(s) only, can use mutliple -s")  # para nargs='+', form a list for args.source
    parser.add_argument("-md", "--mode", type=str, help="only regen modi file for specified source only")
    parser.add_argument("-m", "--max-titles", type=int, help="limit the max titles")
    parser.add_argument("-l", "--url", action="store_true", help="parse from conf_test/urls.txt")
    args = parser.parse_args()
    if len(args.source) > 3:
        print('only max 3 sources are allowed')
    if args.max_titles > 100:
        print('max-titles is now allowed to be over 100')
   
    return args

def parse_args():
    """
        parse arguments
        return: the first argv str if there are any passed arguments; None if no argument is passed
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--source", type=str, nargs='+', help="enable the specified source(s) only, can use mutliple -s")  # para nargs='+', form a list for args.source
        parser.add_argument("-md", "--mode", type=str, help="only regen modi file for specified source only")
        parser.add_argument("-m", "--max-titles", type=int, help="limit the max titles")
        parser.add_argument("-l", "--url", action="store_true", help="parse from conf_test/urls.txt")
        args = parser.parse_args()        
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", type=str, help="specify the basename of json file which is in directory of './input', without extension name")

    args = parser.parse_args()
    if args.name is None:
        raise ValueError('must specify parameter name')
    return args