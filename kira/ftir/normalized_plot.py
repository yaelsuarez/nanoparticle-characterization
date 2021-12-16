from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np

#CO3 value
x_start_CO3 = 1400
x_stop_CO3 = 1600

#PO3 value 
x_start_PO4 = 900
x_stop_PO4 = 1100

#Graph format
x_label = "Wavenumber (cm$^{-1}$)"
y_label = "Absorbance [a.u.]"
graph_title = ""
legend_title = "Ca/P ratio"
lower_x_lim = 400
upper_x_lim = 2500
lower_y_lim = -0.03
upper_y_lim = 1.5


def plot_many_ftir(title, *file_paths, xlabel=x_label, ylabel=y_label):
    """Returns a figure"""
    fig = plt.figure()
    #ax, unused = fig.subplots(2, 1, sharex=True) # This can create multiple plots in a single figure
    ax = fig.subplots(sharex=True)
    for fp,l in file_paths:
        x, y = read_asp(fp) 
        PO4_CO3_ratio = ratio_CO3(x,y,x_start_CO3, x_start_PO4, x_stop_CO3, x_stop_PO4)
        print("CO3/PO4 ratio of", l, " = ",PO4_CO3_ratio)
        ax.plot(x,y, label=l)
           
    ax.set_title(title)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    plt.xlim(lower_x_lim, upper_x_lim)
    plt.ylim(lower_y_lim, upper_y_lim)
    plt.legend(title=legend_title, fontsize=12, title_fontsize=14, loc='upper left')
    ax.invert_xaxis()
    return fig


fig_many_ftir = plot_many_ftir(graph_title,
(r"C:\Users\YaelSuarez\OneDrive\OneDrive - Karolinska Institutet\Documents\KI\Experiments\FTIR\CaP 1.67 ratio 2 to 1 solvent 3 to 8 flame 08_11_21_2021-11-09T11-40-50.asp", "T PLGA"),
(r"C:\Users\YaelSuarez\OneDrive\OneDrive - Karolinska Institutet\Documents\KI\Experiments\FTIR\CaP 2.19 ratio 1 to 1 solvent 3 to 8 flame 18_10_21_Vasia 1.asp", "PLGA" )
)