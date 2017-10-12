import numpy as np


class Researcher:

    def __init__(self):
        self._eps = 0.001
        self._a = -10
        self._b = 10

    @staticmethod
    def function(x):
        return 5 - ((2 - 18 * 5 * x) + 16 * (5 * x) ** 2) / (1 + 5 * x ** 4)

    def calculate_integral(self, a=-10, b=10):

        """ method of medium rectangles """

        result = 0
        current_pos = a
        while current_pos < b:
            result += self._eps * self.function(current_pos + self._eps / 2)
            current_pos += self._eps

        return result

    def find_zeroes(self):

        """ method of chords
        Using graphic we found the following intervals
        which contain zeroes of the function: """

        intervals = [[-5, -3], [-1, 0], [0.175, 1], [3, 5]]
        result = []

        i = 0
        while i < 4:
            x_0 = intervals[i][0]
            x_1 = intervals[i][1]

            f_0 = self.function(x_0)
            f_1 = self.function(x_1)
            while np.abs(f_1) > self._eps:
                x_1 = x_1 - f_1 / (f_1 - f_0) * (x_1 - x_0)
                f_1 = self.function(x_1)
            result.append(x_1)
            i += 1

        return result

    @staticmethod
    def diff_function(x):
        return x

    def get_eps(self):
        return self._eps
