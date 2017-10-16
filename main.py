import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QLabel, QLineEdit, QScrollArea, QScrollBar, QTextEdit
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np
import researcher as res


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # Параметры главного окна
        self.left = 10
        self.top = 10
        self.title = 'Graphic Researcher'
        self.width = 800
        self.height = 650

        # Границы интервала
        self.a = -10.0
        self.b = 10.0
        # Текущее значение х для рассчета функции и производной
        self.x = ''
        self.solver = res.Researcher()

        # Инициализация текстовых полей и кнопок
        self.label_a = QLabel(self)
        self.label_b = QLabel(self)
        self.label_1 = QLabel(self)
        self.label_2 = QLabel(self)
        self.label_3 = QLabel(self)
        self.line_edit_a = QLineEdit(self)
        self.line_edit_b = QLineEdit(self)
        self.line_edit_1 = QLineEdit(self)
        self.line_edit_2 = QTextEdit(self)
        self.line_edit_3 = QLineEdit(self)
        self.line_edit_4 = QLineEdit(self)
        self.line_edit_5 = QLineEdit(self)
        self.line_edit_6 = QLineEdit(self)
        self.button_1 = QPushButton('Calculate integral', self)
        self.button_2 = QPushButton('Find zeroes', self)
        self.button_3 = QPushButton('Draw f(x)', self)
        self.button_4 = QPushButton('Draw f\'(x)', self)
        self.button_5 = QPushButton('Clean', self)
        self.button_6 = QPushButton('Calculate', self)
        self.button_7 = QPushButton('Draw integral', self)
        self.button_8 = QPushButton('Calculate square', self)

        # Инициализация координатной плоскости
        self.plot = PlotCanvas(self, width=6, height=5)
        # Отрисовка главного окна
        self.initUI()

        # Булевы поля, отвечающие за отрисовку каждого из 3-х графиков
        self._drown_1 = False
        self._drown_2 = False
        self._drown_3 = False

    # Функция, отрисовывающая графический интерфейс программы
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.plot.move(0, 0)

        self.label_a.move(610, 5)
        self.label_a.resize(85, 40)
        self.label_a.setText('A value:')

        self.label_b.move(705, 5)
        self.label_b.resize(85, 40)
        self.label_b.setText('B value:')

        self.line_edit_a.move(610, 50)
        self.line_edit_a.resize(85, 30)
        self.line_edit_a.setText(str(self.a))
        self.line_edit_a.textChanged[str].connect(self.on_changed_a)

        self.line_edit_b.move(705, 50)
        self.line_edit_b.resize(85, 30)
        self.line_edit_b.setText(str(self.b))
        self.line_edit_b.textChanged[str].connect(self.on_changed_b)

        self.button_1.setToolTip('Calculates integral from A to B\n'
                                 'Push to see the result in the field below')
        self.button_1.move(610, 85)
        self.button_1.resize(180, 40)
        self.button_1.clicked.connect(self.calculate_integral)

        self.line_edit_1.move(610, 130)
        self.line_edit_1.resize(180, 30)
        self.line_edit_1.setReadOnly(True)

        self.button_2.setToolTip('Push to see the result in the field below')
        self.button_2.move(610, 175)
        self.button_2.resize(180, 40)
        self.button_2.clicked.connect(self.find_zeroes)

        self.line_edit_2.move(610, 220)
        self.line_edit_2.resize(180, 100)
        self.line_edit_2.setReadOnly(True)

        self.button_3.setToolTip('Push to draw graphic')
        self.button_3.move(610, 335)
        self.button_3.resize(180, 40)
        self.button_3.clicked.connect(self.draw_function)

        self.button_4.setToolTip('Push to draw graphic')
        self.button_4.move(610, 390)
        self.button_4.resize(180, 40)
        self.button_4.clicked.connect(self.draw_derivative)

        self.button_5.setToolTip('Push to clean all the fields')
        self.button_5.move(610, 500)
        self.button_5.resize(180, 40)
        self.button_5.clicked.connect(self.clean_all)

        self.label_1.move(10, 510)
        self.label_1.resize(50, 40)
        self.label_1.setText('x = ')

        self.label_2.move(10, 555)
        self.label_2.resize(50, 40)
        self.label_2.setText('f(x) = ')

        self.label_3.move(10, 600)
        self.label_3.resize(50, 40)
        self.label_3.setText('f\'(x) = ')

        self.line_edit_3.move(70, 510)
        self.line_edit_3.resize(160, 30)
        self.line_edit_3.textChanged[str].connect(self.on_changed_1)

        self.line_edit_4.move(70, 555)
        self.line_edit_4.resize(160, 30)
        self.line_edit_4.setReadOnly(True)

        self.line_edit_5.move(70, 600)
        self.line_edit_5.resize(160, 30)
        self.line_edit_5.setReadOnly(True)

        self.button_6.setToolTip('Push to calculate f(x) and f\'(x) values')
        self.button_6.move(240, 600)
        self.button_6.resize(100, 40)
        self.button_6.clicked.connect(self.calculate)

        self.button_7.setToolTip('Push to draw integral')
        self.button_7.move(610, 445)
        self.button_7.resize(180, 40)
        self.button_7.clicked.connect(self.draw_integral)

        self.button_8.setToolTip('Push to see the result in the field below')
        self.button_8.move(350, 510)
        self.button_8.resize(160, 40)
        self.button_8.clicked.connect(self.calc_square)

        self.line_edit_6.move(350, 560)
        self.line_edit_6.resize(160, 30)
        self.line_edit_6.setReadOnly(True)

        self.show()

    # Метод, реагирующий на ввод пользователем левой границы интервала
    def on_changed_a(self, text):
        if len(text) == 0:
            return
        if text[0] == '-' and len(text) == 1:
            return
        if float(text) < -10:
            self.line_edit_a.setText('-10.0')
            self.a = -10.0
        else:
            self.a = float(text)

    # Метод, реагирующий на ввод пользователем правой границы интервала
    def on_changed_b(self, text):
        if len(text) == 0:
            return
        if text[0] == '-' and len(text) == 1:
            return
        if float(text) > 10:
            self.line_edit_b.setText('10.0')
            self.b = 10.0
        else:
            self.b = float(text)

    # Метод, реагирующий на ввод пользователем значения х
    def on_changed_1(self, text):
        self.x = text

    # Метод, очищающий все текстовые поля
    @pyqtSlot()
    def clean_all(self):
        self.line_edit_1.clear()
        self.line_edit_2.clear()
        self.line_edit_a.setText('-10.0')
        self.line_edit_b.setText('10.0')
        self.line_edit_3.clear()
        self.line_edit_4.clear()
        self.line_edit_5.clear()
        self.line_edit_6.clear()

    # Метод, рассчитывающий интеграл
    @pyqtSlot()
    def calculate_integral(self):
        # Проверка интервала на корректность
        if self.a > self.b:
            self.line_edit_1.setText('Wrong params')
            return
        result = self.solver.calculate_integral(a=self.a, b=self.b)
        # Вывод результата
        self.line_edit_1.setText(str(result))

    # Метод, рассчитывающий корни уравнения
    @pyqtSlot()
    def find_zeroes(self):
        zeroes = self.solver.find_zeroes()
        result = ""
        for i in np.arange(len(zeroes)):
            result = result + str(zeroes[i]) + '\n'
        # Вывод результата
        self.line_edit_2.setText(result)
        # Отрисовка точек на координатной плоскости
        self.plot.add_scatter(zeroes, np.zeros(len(zeroes)))

    # Метод, русующий график функции
    @pyqtSlot()
    def draw_function(self):
        if not self._drown_1:
            self._drown_1 = True
            self.plot.plot(self.solver.function, 'f(x)')
        else:
            return

    # Метод, русующий график производной
    @pyqtSlot()
    def draw_derivative(self):
        if not self._drown_2:
            self._drown_2 = True
            self.plot.plot(self.solver.diff_function, 'f\'(x)')
        else:
            return

    # Метод, рассчитывающий значения функции и ее производной в конкретной точке
    @pyqtSlot()
    def calculate(self):
        if len(self.x) == 0:
            return
        else:
            x = float(self.x)
            # Вывод результата
            self.line_edit_4.setText(str(self.solver.function(x)))
            self.line_edit_5.setText(str(self.solver.diff_function(x)))

    # Метод, русующий график итеграла
    @pyqtSlot()
    def draw_integral(self):
        if not self._drown_3:
            self._drown_3 = True
            self.plot.plot_integral(self.solver.calculate_integral, '$\int_{-10}^{x} f(x)dx$')
        else:
            return

    # Метод, рассчитывающий площадь под графиком функции
    @pyqtSlot()
    def calc_square(self):
        zeroes = self.solver.find_zeroes()
        result = self.solver.calculate_integral(a=zeroes[1], b=zeroes[2])
        # Вывод результата
        self.line_edit_6.setText(str(result))


# Класс, отвечающий за отрисовку координатной плоскости и графиков
class PlotCanvas(FigureCanvas):
    # Инициализация
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.add_grid()

    # Метод, рисующий график функции и подписывающий его
    def plot(self, func, name=''):
        ax = self.figure.add_subplot(111)
        x = np.arange(-10, 10, 0.1)
        ax.plot(x, func(x), label=name)
        ax.set_title('Coordinate plane')
        ax.legend()
        self.draw()

    # Метод для отрисовки графика интеграла
    def plot_integral(self, func, name=''):
        ax = self.figure.add_subplot(111)
        x = np.arange(-10, 10, 0.1)
        y = []
        for i in x:
            if i > -10:
                y.append(func(a=i-0.1, b=i))
            else:
                y.append(0)
        y = np.array(y)
        y = np.cumsum(y)
        ax.plot(x, y, label=name)
        ax.set_title('Coordinate plane')
        ax.legend()
        self.draw()

    # Метод, добавляющий сетку на координатную плоскость
    def add_grid(self):
        ax = self.figure.add_subplot(111)
        ax.grid()

    # Метод, отрисовывающий точки на координатной плоскости
    def add_scatter(self, x, y):
        ax = self.figure.add_subplot(111)
        ax.scatter(x, y)
        self.draw()


# Основная функция, выполняющаяся при запуске программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())




