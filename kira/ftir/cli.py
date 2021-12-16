from argparse import ArgumentParser
from kira.ftir.utils import read_asp, auc_ratio
import sys


def calc_ratio(raw_args):
    parser = ArgumentParser("FTIR ratio two peaks")
    parser.add_argument("-f", type=str)

    #CO3 value
    x_start_b = 1400
    x_stop_b = 1600
    #PO3 value 
    x_start_a = 900
    x_stop_a = 1100

    args = parser.parse_args(raw_args)
    x,y = read_asp(args.f)
    ratio_a_b = auc_ratio(x,y,x_start_b, x_start_a, x_stop_b, x_stop_a)
    print(ratio_a_b)


calc_ratio(sys.argv[1:])
print(sys.argv)

