import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
import numpy as np
import researcher as res


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window parameters
        self.left = 10
        self.top = 10
        self.title = 'Graphic Researcher'
        self.width = 800
        self.height = 640

        # Borders of the interval and Researcher object
        self.a = -10.0
        self.b = 10.0
        self.solver = res.Researcher()

        # Window fields and buttons
        self.label_a = QLabel(self)
        self.label_b = QLabel(self)
        self.line_edit_a = QLineEdit(self)
        self.line_edit_b = QLineEdit(self)
        self.line_edit_1 = QLineEdit(self)
        self.line_edit_2 = QLineEdit(self)
        self.button_1 = QPushButton('Calculate integral', self)
        self.button_2 = QPushButton('Find zeroes', self)
        self.button_3 = QPushButton('Draw f(x)', self)
        self.button_4 = QPushButton('Draw f\'(x)', self)
        self.button_5 = QPushButton('Clean', self)
        self.plot = PlotCanvas(self, width=6, height=5)
        self.initUI()

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
        self.line_edit_2.resize(180, 30)
        self.line_edit_2.setReadOnly(True)

        self.button_3.setToolTip('Push to draw graphic')
        self.button_3.move(610, 265)
        self.button_3.resize(180, 40)
        self.button_3.clicked.connect(self.draw_function)

        self.button_4.setToolTip('Push to draw graphic')
        self.button_4.move(610, 320)
        self.button_4.resize(180, 40)
        self.button_4.clicked.connect(self.draw_derivative)

        self.button_5.setToolTip('Push to clean all the fields')
        self.button_5.move(610, 375)
        self.button_5.resize(180, 40)
        self.button_5.clicked.connect(self.clean_all)

        self.show()

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

    @pyqtSlot()
    def clean_all(self):
        self.line_edit_1.clear()
        self.line_edit_2.clear()
        self.line_edit_a.setText('-10.0')
        self.line_edit_b.setText('10.0')

    @pyqtSlot()
    def calculate_integral(self):
        if self.a > self.b:
            self.line_edit_1.setText('Wrong params')
            return
        result = self.solver.calculate_integral(a=self.a, b=self.b)
        self.line_edit_1.setText(str(result))

    @pyqtSlot()
    def find_zeroes(self):
        zeroes = self.solver.find_zeroes()
        result = ""
        for i in np.arange(len(zeroes)):
            result = result + str(zeroes[i]) + '\n'
        self.line_edit_2.setText(result)

    @pyqtSlot()
    def draw_function(self):
        self.plot.plot(self.solver.function)

    def draw_derivative(self):
        self.plot.plot(self.solver.diff_function)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # self.plot()

    def plot(self, func):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        #ax.plot(data, 'r-')
        ax.grid()
        x = np.arange(-10, 10, 0.1)
        ax.plot(x, func(x))
        ax.set_title('Coordinate plane')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())




