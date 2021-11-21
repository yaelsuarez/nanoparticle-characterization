from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

# CO3 value
x_start_CO3 = 1400
x_stop_CO3 = 1600

# PO3 value
x_start_PO3 = 900
x_stop_PO3 = 1100

# Graph format
x_label = "Wavenumber (cm$^{-1}$)"
y_label = "Absorbance"
graph_title = "FTIR"
lower_x_lim = 400
upper_x_lim = 3000
lower_y_lim = 0
upper_y_lim = 1


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
        # TO NORMALIZE
        # y_data = [(i - min(y_data))/(max(y_data)- min(y_data)) for i in y_data]
        assert (
            len(y_data) == n_data_points
        ), f"The number of expected y_values is {n_data_points}, but {len(y_data)} were found"
    x = np.linspace(x_start, x_end, n_data_points)
    y = np.array(y_data)
    return x, y


def plot_many_ftir(title, *file_paths, xlabel=x_label, ylabel=y_label):
    """Returns a figure"""
    fig = plt.figure()
    # ax, unused = fig.subplots(2, 1, sharex=True) # This can create multiple plots in a single figure
    ax = fig.subplots(sharex=True)
    for fp, l in file_paths:
        x, y = read_asp(fp)
        auc_CO3 = auc_value(x, y, x_start_CO3, x_stop_CO3)
        auc_PO3 = auc_value(x, y, x_start_PO3, x_stop_PO3)
        PO3_CO3_ratio = auc_CO3 / auc_PO3
        print("CO3/PO3 ratio of", l, " = ", PO3_CO3_ratio)
        ax.plot(x, y, label=l)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(which="both", axis="both")
    plt.xlim(lower_x_lim, upper_x_lim)
    plt.ylim(lower_y_lim, upper_y_lim)
    plt.legend()
    # fig.savefig(line_name)

    return fig, auc_PO3


def auc_value(x, y, x_start, x_stop):
    x_positions = []
    y_values = []
    x_positions = np.where((x < x_stop) & (x > x_start))
    y_values = [y[i] for i in x_positions]
    auc = np.trapz(y_values)
    return auc


fig_many_ftir, auc = plot_many_ftir(
    graph_title,
    (
        r"C:\Users\YaelSuarez\OneDrive\OneDrive - Karolinska Institutet\Documents\KI\Experiments\FTIR\Powder samples\Sample 1 10_5 1_1 0.4 2.asp",
        "10:5 flame 1:1 solvent",
    ),
    (
        r"C:\Users\YaelSuarez\OneDrive\OneDrive - Karolinska Institutet\Documents\KI\Experiments\FTIR\Powder samples\Sample 2 10_5 2_1 0.4 2.asp",
        "10:5 flame 2:1 solvent",
    ),
    (
        r"C:\Users\YaelSuarez\OneDrive\OneDrive - Karolinska Institutet\Documents\KI\Experiments\FTIR\Powder samples\Sample 3 3_8 1_1 0.1 2.asp",
        "3:8 flame 1:1 solvent",
    ),
    (
        r"C:\Users\YaelSuarez\OneDrive\OneDrive - Karolinska Institutet\Documents\KI\Experiments\FTIR\Powder samples\Sample 4 3_8 2_1 0.4 1.asp",
        "3:8 flame 2:1 solvent",
    ),
)
