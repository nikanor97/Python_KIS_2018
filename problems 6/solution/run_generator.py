from dialogsgenerator import randomdialog
from dialogsgenerator import agent
import pandas as pd
import sys
import argparse

def generate(rd, count_dialogs=5):
    def generate_generator():
        for i in range(count_dialogs):
            yield next(rd.generate())
    return generate_generator()


def write(dialogs, target):
    cnt = -1
    try:
        while True:
            cnt += 1
            res = next(dialogs)
            print('____________________Dialog ' + str(cnt) + '____________________', file=target)
            for turn_num in range(len(res)):
                print("turn ", turn_num, ':', file=target)
                for phrase in res[turn_num]:
                    print(phrase, file=target)
    except StopIteration:
        pass




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate dialogs')
    parser.add_argument('count_dialogs', type=int, help='Number of dialogs to be generated')
    parser.add_argument('max_dialog_len', type=int, help='Max number of turns in 1 dialog')
    parser.add_argument('-o', '--output', help='Outstream')
    parser.add_argument('-t', '--trump_kb', help='File with Trump`s tweets')
    parser.add_argument('-c', '--clinton_kb', help='File with Clinton`s tweets')

    args = parser.parse_args()

    clinton = pd.read_csv("clinton.csv", encoding="utf-8")
    trump = pd.read_csv("trump.csv", encoding="utf-8")

    rd = randomdialog.RandomDialog([agent.Agent(clinton, "clinton"), agent.Agent(trump, "trump")],
                                   max_len=args.max_dialog_len)

    dialogs = generate(rd, args.count_dialogs)
    write(dialogs, sys.stdout)
