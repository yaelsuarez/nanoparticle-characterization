import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import norm
import os


def create_ref_line(start, stop, samples, scale):
    x = np.linspace(start, stop, samples)
    scale += 5 * np.random.random()
    y = scale * (np.sin(2 * x / (start - stop) + 3.14) +
                 np.random.normal(0, 0.001, samples) + 1)
    return x, y


def get_gaussian(x, scale=None, mu=None, sigma=None):
    scale = 5e4 + 1e5 * np.random.random(
    ) if scale is None else scale + 1e4 * np.random.random() - 5e3
    mu = random.randrange(
        500, 800) if mu is None else mu + 10 * np.random.random() - 5
    sigma = random.randrange(
        1, 50) if sigma is None else sigma + np.random.random()
    print(scale, mu, sigma)
    y2 = scale * norm.pdf(x, mu, sigma)
    return x, y2


def get_luminescence_trace(x):
    _, y = get_gaussian(x)
    for _ in range(5):
        _, y_temp = get_gaussian(x)
        y += y_temp
    return y


def get_luminescence_traces(x, traces: int):
    scales = [5e4 + 1e5 * np.random.random() for _ in range(5)]
    mus = [random.randrange(500, 800) for _ in range(5)]
    sigmas = [random.randrange(1, 50) for _ in range(5)]
    for trace in range(traces):
        y = np.zeros_like(x)
        for scale, mu, sigma in zip(scales, mus, sigmas):
            y += get_gaussian(x, scale, mu, sigma)[1]
        yield y


file_header = lambda name: f'Data from {name}_16-47-09-365.txt Node\nDate: Sun Jun 13 23:27:09 CET 2021\nUser: fcossio\nSpectrometer: FLMS15016\nTrigger mode: 0\nIntegration Time (sec): 3.000000E-1Scans to average: 1\nElectric dark correction enabled: true\nNonlinearity correction enabled: false\nBoxcar width: 0\nXAxis mode: Wavelengths\nNumber of Pixels in Spectrum: 2048\n>>>>>Begin Spectral Data<<<<<\n'


def write_file(path, x, y):
    with open(path, 'w') as file:
        file.write(file_header(os.path.basename(path)))
        for x, y in zip(x, y):
            file.write(f"{x:.3f}\t{y:.3f}\n")


if __name__ == "__main__":
    scale = 500 + 50 * np.random.random()
    for i in range(5):
        x, y = create_ref_line(340.154, 1022.689, 2048, scale)
        write_file(f"reference_meas_2/repetition_{i}.txt", x, y)

    for i, y in enumerate(get_luminescence_traces(x, 5)):
        write_file(f"nanoparticle_C/repetition_{i}.txt", x, y)

    # for i, y in enumerate(get_luminescence_traces(x,5)):
    #     write_file(f"nanoparticle_B/repetition_{i}.txt", x,y)
