import argparse
import json


def data_reader(data_file):
    data = json.load(open(data_file))
    data = [{"question": d['question'], "answer": d['answer']} for d in data]

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()    
    parser.add_argument("--data_file", type=str)
    args = parser.parse_args()

    data = data_reader(args.data_file)

