from argparse import ArgumentParser
from kira.ftir.utils import read_asp, ratio_a_b_peaks
import sys


def calc_ratio(raw_args):
    parser = ArgumentParser("FTIR ratio two peaks")
    parser.add_argument("-f", type=str)
    parser.add_argument("-peak_a", type=int)
    parser.add_argument("-peak_b", type=int)
    parser.add_argument("-range_auc", type=int)

    args = parser.parse_args(raw_args)
    x,y = read_asp(args.f)
    ratio_a_b = ratio_a_b_peaks(x,y,args.peak_a, args.peak_b, args.range_auc)
    print(ratio_a_b)


calc_ratio(sys.argv[1:])
print(sys.argv)

