# Проект сделан Майоровым Александром
# Математическая утилита, стоящая графики, с возможностью использовать параметры
# Также строятся графики производной и первообразной

import sys
from layout import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPlainTextEdit
from PyQt5.QtGui import QFont
from sympy import *  # Библиотека для вычисления производной и первообразной


def frange(start, stop, step):
    """Аналог range, но с возможность использовать float"""

    i = start
    while i < stop:
        yield i
        i += step


class Function:
    """Класс функция"""

    def __init__(self, function, parameters=""):
        """Конструктор класса"""
        self.function = function
        self.parameters = parameters
        self._parsing()

    def _parsing(self):
        """Обработка параметров"""

        if self.parameters != "":
            self.parameters = [i.split('=') for i in self.parameters.split(',')]
            for i in self.parameters:
                self.function = self.function.replace(i[0], i[1])

    def build(self, pl, start, end):
        """Функция, строящая графики"""

        self.s = start
        self.t = end
        pl.clear()
        self.values = []

        for i in frange(float(self.s), float(self.t + 1), 0.5):
            x = i
            try:
                self.values.append(float(eval(self.function)))
            except Exception as e:
                self.values.append(0)
                print(str(e))

        pl.plot([i for i in frange(float(self.s), float(self.t + 1), 0.5)],
                self.values, pen='w')


class Derivative(Function):
    """Класс производная(наследник класса функция)"""

    def __init__(self, function, parameters=""):
        """Конструктор класса(отличается от консруктора класса функции)"""

        self.function = function
        self.parameters = parameters
        self._parsing()
        x = Symbol("x")
        self.function = str(eval(self.function.replace("x", "Symbol('x')")).diff(x))


class Antiderivative(Function):
    """Класс первообразная(наследник класса функция)"""

    def __init__(self, function, parameters=""):
        """Конструктор класса(отличается от консруктора класса функции)"""
        self.function = function
        self.parameters = parameters
        self._parsing()
        self.function = integrate(self.function).__repr__()


class MyWidget(QMainWindow, Ui_MainWindow):
    """Главный класс окна"""

    def __init__(self):
        """Конструктор класса"""

        super().__init__()
        self.setupUi(self)  # Подключение основных элементов интерфейса
        self.setWindowTitle('Математическая утилита')
        try:
            self.pushButton.clicked.connect(self.run)
            self.pushButton_2.clicked.connect(self.show_info)
        except Exception as e:
            print(str(e))

    def run(self):
        """Главные вычисления"""

        try:

            self.function = Function(self.func.text(), parameters=self.params.text())
            self.function.build(self.graphic, float(self.start.text()), float(self.to.text()))

            self.antiderivative = Antiderivative(self.func.text(), parameters=self.params.text())
            self.antiderivative.build(self.antideriv_gr, float(self.start.text()),
                                      float(self.to.text()))

            self.derivative = Derivative(self.func.text(), parameters=self.params.text())
            self.derivative.build(self.deriv_gr, float(self.start.text()), float(self.to.text()))

            self.derivative_output.clear()
            self.antiderivative_output.clear()

            self.function_output.setText("f(x):" + self.function.function)
            self.derivative_output.setText("f′(x):" + self.derivative.function)
            self.antiderivative_output.setText(
                "F(x):" + self.antiderivative.function + " + C")


        except Exception as e:
            print(str(e))

    def show_info(self):
        """Функция, отвечающая за работу кнопки Помощь"""

        try:
            self.newfont = QFont("MS Shell Dlg 2", 10, QFont.Bold)
            self.show_info_window = QMainWindow()
            self.show_info_window.setGeometry(300, 300, 600, 500)
            self.show_info_window.setWindowTitle('Помощь')
            self.show_info_window.setEnabled(False)
            self.show_info_window.setFont(self.newfont)
            self.help_text = QPlainTextEdit(self.show_info_window)
            self.help_text.setGeometry(20, 20, 560, 460)
            self.help_text.appendPlainText(
                "Вас приветсвует математическая утилита\n" +
                "Тут вы можете строить графики функций,\n" +
                "их производных и первообразных с параметрами\n\n" +
                "Вводите функцию, как в python\n" +
                "Например, 2*x**3 или (x**a)/b*c\n\n" +
                "Параметры вводите в следующем формате\n" +
                "параметр1=значение1,параметр2=значение2,параметрi=значениеi\n" +
                "Например,\n" +
                "a=2,b=3,c=6\n\n" +
                "Основные функции:\n" +
                "умножение -> *\n" +
                "вычитание -> -\n" +
                "деление -> /\n" +
                "сложение -> +\n" +
                "возведение в степень -> **\n" +
                "корень из x -> sqrt(x)\n" +
                "синус из x -> sin(x)\n" +
                "косинус из x -> cos(x)\n" +
                "тангенс из x -> tan(x)\n\n" +
                "При построении графиков ОБЯЗАТЕЛЬНО укажите ограничения " +
                "для x в самых верхних полях ввода\n"
            )
            self.show_info_window.show()
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = MyWidget()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))
