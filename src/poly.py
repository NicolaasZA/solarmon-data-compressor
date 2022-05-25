# This library requires numpy
# - pip install numpy

import numpy as np
from numpy.polynomial.polynomial import Polynomial


def polynomial_coefficients(xs, coeffs):
    """ Returns a list of function outputs (`ys`) for a polynomial with the given coefficients and
    a list of input values (`xs`).

    The coefficients must go in order from a0 to an, and all must be included, even if the value is 0.
    """
    order = len(coeffs)
    print(f'# This is a polynomial of order {order - 1}.')

    # Initialise an array of zeros of the required length.
    ys = np.zeros(len(xs))
    for i in range(order):
        ys += coeffs[i] * xs ** i
    return ys


def smoothData(data: list[float], size=5) -> list[float]:
    smoothed: list[float] = []

    for x in range(0, len(data)-size, size):
        new_y = 0
        for xa in range(0, size):
            new_y += data[x + xa]
        new_y = new_y / size
        smoothed.append(new_y)
    return smoothed


def trimData(data: list[float], lower_limit=6) -> list[float]:
    if lower_limit < 0:
        lower_limit = 0

    start_x = 0
    end_x = len(data) - 1
    while data[start_x] <= lower_limit:
        start_x += 1
    while (data[end_x] <= lower_limit) and (end_x > start_x):
        end_x -= 1

    return data[start_x:end_x]


def findPolynomial(data: list[float]) -> Polynomial:
    """
    Take an array of data points, and smooth them out. Then, generate a polynomial that fits the smoothed points.
    """
    if data == None or len(data) == 0:
        return None

    return Polynomial.fit(range(0, len(data)), data, deg=2)


def findPolyNP(y: list[float], deg=2) -> Polynomial:
    exes = [x for x in range(0, len(y))]
    return np.polyfit(exes, y, deg)
