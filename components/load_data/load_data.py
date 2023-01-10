import argparse
import json
from utils_io import Tools


def data_reader(data_file, output_dir):
    data = json.load(open(data_file))
    data = [{"question": d['question'], "answer": d['answer']} for d in data]

    Tools.dump_pickle(os.path.join(output_dir, "data.pkl"), data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()    
    parser.add_argument("--data_file", type=str)
    parser.add_argument("--output_dir", type=str)
    args = parser.parse_args()

    data_reader(args.data_file, args.output_dir)

