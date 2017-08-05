import json
import argparse


def parse_json(json_filename, arg_path):
    with open(json_filename) as data_file:
        json_as_dict = json.load(data_file)

    for key in arg_path.split(","):
        json_as_dict = json_as_dict.get(key)
        if json_as_dict is None:
            raise ValueError("JSON does not contain dict path {}. Only got to key '{}'".format(arg_path, key))

    return json_as_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--json_filename', type=str,
                        help='a json file to parse')
    parser.add_argument('--arg_path', type=str,
                        help="keys , subkeys, subsubkeys etc.")

    args = parser.parse_args()
    print parse_json(args.json_filename, args.arg_path)
