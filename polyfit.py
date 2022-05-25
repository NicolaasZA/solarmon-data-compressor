from src.poly import smoothData, trimData, findPolyNP
from src.files import fileToLines

import numpy as np
from matplotlib import pyplot as plt

data = []
raw = fileToLines('input/okahandja_2022_5_23.csv')
for r in raw:
    if not r.startswith('DATE'):
        pieces = r.split(',')
        if len(pieces) >= 9:
            data.append(float(pieces[7]))

data = trimData(data, 30)


data_10 = smoothData(data, 10)
data_50 = smoothData(data, 50)
data_100 = smoothData(data, 100)


def plot_data(pvc_data, deg, cc, rc, row, title = True):
    org_len = len(pvc_data)

    # 20%
    oq = int(len(pvc_data)/10)*2
    oq_data = pvc_data[:oq]
    oq_fit = findPolyNP(oq_data, deg)
    oq_fit_x = np.linspace(0, org_len, num=50)
    oq_fit_poly = np.poly1d(oq_fit)
    oq_fit_y = oq_fit_poly(oq_fit_x)

    # 50%
    half = int(len(pvc_data)/10)*5
    half_data = pvc_data[:half]
    half_fit = findPolyNP(half_data, deg)
    half_fit_x = np.linspace(0, org_len, num=50)
    half_fit_poly = np.poly1d(half_fit)
    half_fit_y = half_fit_poly(half_fit_x)

    # 60%
    tq = int(len(pvc_data)/3) * 6
    tq_data = pvc_data[:tq]
    tq_fit = findPolyNP(tq_data, deg)
    tq_fit_x = np.linspace(0, org_len, num=50)
    tq_fit_poly = np.poly1d(tq_fit)
    tq_fit_y = tq_fit_poly(tq_fit_x)

    # fig, axs = plt.subplots(2)
    # axs[0].plot(range(0, len(half_data)), half_data, 'o', half_fit_x, half_fit_y)
    # axs[1].plot(range(0, len(tq_data)), tq_data, 'o', tq_fit_x, tq_fit_y)

    plt.subplot(cc, rc, (cc*(row-1)) + 1)
    plt.plot(range(0, len(oq_data)), oq_data, 'o', oq_fit_x, oq_fit_y)
    if title:
        plt.title('20%')

    plt.subplot(cc, rc, (cc*(row-1)) + 2)
    plt.plot(range(0, len(half_data)), half_data, 'o', half_fit_x, half_fit_y)
    if title:
        plt.title('50%')

    plt.subplot(cc, rc, (cc*(row-1)) + 3)
    plt.plot(range(0, len(tq_data)), tq_data, 'o', tq_fit_x, tq_fit_y)
    if title:
        plt.title('60%')


plot_data(data_100, 2, 3, 3, 1)
plot_data(data_100, 3, 3, 3, 2, False)
plot_data(data_100, 7, 3, 3, 3, False)
plt.show()
