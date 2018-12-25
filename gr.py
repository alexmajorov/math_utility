##Проект сделан Майоровым Александром
##Математическая утилита, стоящая графики, с возможностью использовать параметры
##Также строятся графики производной и первообразной

import sys
from layout import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from sympy import *


def derivative(func):
    """Определение производной"""

    x = Symbol("x")
    return str(eval(func.replace("x", "Symbol('x')")).diff(x))


def antiderivative(func):
    """Определение первообразной"""

    return integrate(func).__repr__()


def frange(start, stop, step):
    """Аналог range, но с возможность использовать float"""

    i = start
    while i < stop:
        yield i
        i += step


class MyWidget(QMainWindow, Ui_MainWindow):
    """Главный класс окна"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        try:
            self.pushButton.clicked.connect(self.run)
        except Exception as e:
            print(str(e))

    def run(self):
        """Главные вычисления"""

        try:
            
            """Работа с параметрами"""
            
            self.parameters = self.params.text().split(",")
            
            for i in range(len(self.parameters)):
                self.parameters[i] = self.parameters[i].split("=")

            self.function = self.func.text()
            if [''] not in self.parameters:
                for i in self.parameters:
                    self.function = self.function.replace(i[0], i[1])
                
            self.derivative_output.clear()
            self.antiderivative_output.clear()

            self.s = int(self.start.text())
            self.t = int(self.to.text())

            """Простроение графиков"""

            self.build(self.function, self.graphic)
            self.build(derivative(self.function), self.deriv_gr)
            self.build(antiderivative(self.function), self.antideriv_gr)

            """Вывод текста в окне"""

            self.derivative_output.appendPlainText("f′(x):" + derivative(self.function))
            self.antiderivative_output.appendPlainText("F(x):" + antiderivative(self.function))

        except Exception as e:
            print(str(e))

    def build(self, func, pl):
        """Функция, строящая графики"""

        pl.clear()
        self.values = []

        for i in frange(float(self.s), float(self.t + 1), 0.5):
            x = i
            try:
                self.values.append(float(eval(func)))
            except Exception as e:
                self.values.append(0)
                print(str(e))

        pl.plot([i for i in frange(float(self.s), float(self.t + 1), 0.5)],
                self.values, pen='w')


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = MyWidget()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))
