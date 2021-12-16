from typing import Tuple
import numpy as np


def read_asp(file_path: str) -> Tuple[np.array, np.array]:
    """
    Read an asp file created with X machine
    Args:
        file_path: the path pointing towards a text file that has
        the following format:
            line 0: number of points (int)
            line 1: x_start (float)
            line 2: x_end (float)
            line 3: ? (int)
            line 4: ? (int)
            line 5: ? (int)
            lines 6-end: y_data (float)
    return: tuple with two numpy arrays (x, y)
    """
    with open(file_path, mode="r") as file:
        n_data_points = int(next(file))
        x_start = float(next(file))
        x_end = float(next(file))
        _ = int(next(file))  # only specified to ignore those lines
        _ = int(next(file))
        _ = int(next(file))
        y_data = [float(i) for i in file]
        assert (
            len(y_data) == n_data_points
        ), f"The number of expected y_values is {n_data_points}, but {len(y_data)} were found"
    x = np.linspace(x_start, x_end, n_data_points)
    y = np.array(y_data)
    return x, y

def ratio_a_b_peaks(x,y,peak_a, peak_b, range_auc):
    x_start_a = peak_a - range_auc
    x_stop_a = peak_a + range_auc
    x_start_b = peak_b - range_auc
    x_stop_b = peak_b + range_auc
    auc_a = auc_value(x,y,x_start_a, x_stop_a)
    auc_b = auc_value(x,y,x_start_b, x_stop_b)
    a_b_ratio = auc_b/auc_a
    return  a_b_ratio

def auc_value(x, y, x_start, x_stop):
    """Find AUC by trapz method"""
    x_positions = []
    y_values = []
    x_positions = np.where((x < x_stop) & (x > x_start))
    y_values = [y[i] for i in x_positions]
    auc = np.trapz(y_values)
    return auc