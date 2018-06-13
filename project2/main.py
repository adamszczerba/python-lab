import json
import argparse
from parser import *
import sys


def main():
    parser = argparse.ArgumentParser(description=
                                     'Process json to png or show it on screen')
    # optional argument
    parser.add_argument('-o', '--output', metavar='png_file_name',
                        default=None, help='save result as png file')
    # positional argument
    parser.add_argument('json_file_name', help='json file, you want to process')
    args = parser.parse_args()

    try:
        with open(args.json_file_name, 'r') as f:
            json_content = json.load(f)
    except FileNotFoundError:
        print("not found input file")
        sys.exit(1)


    try:
        data_from_json = Parser(json_content)
    except KeyError:
        print("invalid figure type")
        sys.exit(1)
    except SyntaxError:
        print("invalid color format")
        sys.exit(1)

    to_ret = data_from_json.process_to_picture()

    if args.output is None:
        to_ret.show()
    else:
        to_ret.save(args.output)


if __name__ == "__main__":
    main()
