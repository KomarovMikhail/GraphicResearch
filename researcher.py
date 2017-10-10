import numpy as np


class Researcher:

    def __init__(self):
        self._eps = 0.01
        self._a = -10
        self._b = 10

    def function(self, x):
        return 5 - ((2 - 18 * 5 * x) + 16 * (5 * x) ** 2) / (1 + 5 * x ** 4)

    def calculate_integral(self):
        result = 0
        current_pos = self._a
        while current_pos < self._b:
            result += self._eps * self.function(current_pos + self._eps / 2)
            current_pos += self._eps
        return result

    def find_zeroes(self):
        result = []
        return result

    def diff_function(self, x):
        return x

    def get_eps(self):
        return self._eps
