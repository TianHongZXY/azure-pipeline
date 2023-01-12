import os
import json
import argparse
from utils_io import Tools


def data_reader(data_dir, output_dir):
    for file in os.listdir(data_dir):
        if "hotpotqa" not in file:
            continue
        data = json.load(open(os.path.join(data_dir, file)))
        data = [{"question": d['question'], "answer": d['answer']} for d in data]
        Tools.dump_pickle(os.path.join(output_dir, f"{file}-data.pkl"), data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()    
    parser.add_argument("--data_dir", type=str)
    parser.add_argument("--output_dir", type=str)
    args = parser.parse_args()

    data_reader(args.data_dir, args.output_dir)

