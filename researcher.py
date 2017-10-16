import numpy as np


class Researcher:

    # Инициализация класса
    def __init__(self):
        # Допустимая погрешность
        self._eps = 0.0001

    @staticmethod
    # Исследуемая функция
    def function(x):
        return 5 - ((2 - 18 * 5 * x) + 16 * (5 * x)**2) / (1 + 5 * x**4)

    # Рассчет интеграла в заданных пределах
    def calculate_integral(self, a=-10, b=10):

        """ method of medium rectangles """

        result = 0
        current_pos = a
        while current_pos < b:
            result += self._eps * self.function(current_pos + self._eps / 2)
            current_pos += self._eps

        return result

    # Поиск нулей функции
    def find_zeroes(self):

        """ method of chords
        Using graphic we found the following intervals
        which contain zeroes of the function: """

        # Интервалы, содержащие нули функции
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
    # Производная функции
    def diff_function(x):
        return 2 * 5 * (16 * 5**2 * x**5 - 5 * (27 * x**3 + 16) * x + 4 * x**3 + 9) / (5 * x**4 + 1)**2

    # Функция, возвращающая значение погрешности
    def get_eps(self):
        return self._eps
