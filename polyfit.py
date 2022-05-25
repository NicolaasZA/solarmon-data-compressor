from src.poly import smoothData, trimData, findPolyNP
from src.files import fileToLines

import numpy as np
from matplotlib import pyplot as plt

data = []
raw = fileToLines('input/okahandja_2022_5_24.csv')
for r in raw:
    if not r.startswith('DATE'):
        pieces = r.split(',')
        if len(pieces) >= 9:
            data.append(float(pieces[7]))

data = trimData(data, 30)


data_10 = smoothData(data, 10)
data_50 = smoothData(data, 50)
data_100 = smoothData(data, 100)

percentages = [20, 30, 40, 50, 60, 70, 80, 90, 100]


def plot_data(data, rc, row, deg, title=True):
    original_length = len(data)
    cc = len(percentages)

    col_index = 1
    for perc in percentages:
        # Trim data
        end_x = int(len(data)*(perc/100.0))
        perc_data = data[:end_x]

        # Calculate fit function
        perc_fit = findPolyNP(perc_data, deg)
        perc_fit_poly = np.poly1d(perc_fit)

        # Generate plot data for fit function
        perc_fit_x = np.linspace(0, original_length, num=50)
        perc_fit_y = perc_fit_poly(perc_fit_x)

        plt.subplot(rc, cc, (cc*(row-1)) + col_index)
        plt.plot(range(0, len(perc_data)), perc_data,
                 'o', perc_fit_x, perc_fit_y)
        col_index += 1
        if title:
            plt.title(f'{perc}%')


plot_data(data_100, 4, 1, 1)
plot_data(data_100, 4, 2, 2, False)
plot_data(data_100, 4, 3, 3, False)
plot_data(data_100, 4, 4, 5, False)
plt.show()
