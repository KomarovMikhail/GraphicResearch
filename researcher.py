import numpy as np


class Researcher:

    def __init__(self):
        self._eps = 0.01
        self._a = -10
        self._b = 10

    def function(self, x):
        return 5 - ((2 - 18 * 5 * x) + 16 * (5 * x) ** 2) / (1 + 5 * x ** 4)

    def calculate_integral(self):

        # method of medium rectangles

        result = 0
        current_pos = self._a
        while current_pos < self._b:
            result += self._eps * self.function(current_pos + self._eps / 2)
            current_pos += self._eps

        return result

    def find_zeroes(self):

        # method of chords

        result = []
        x_0 = self._a
        x_1 = self._a + 1

        x_2 = x_1 - (self.function(x_1) * (x_1 - x_0)) / (self.function(x_1) - self.function(x_0))
        x_0 = x_1
        x_1 = x_2

        while np.abs(self.function(x_2)) > self._eps or np.abs(x_1 - x_0) > self._eps:
            x_2 = x_1 - (self.function(x_1) * (x_1 - x_0)) / (self.function(x_1) - self.function(x_0))
            x_0 = x_1
            x_1 = x_2
        result.append(x_2)

        return result

    def diff_function(self, x):
        return x

    def get_eps(self):
        return self._eps
