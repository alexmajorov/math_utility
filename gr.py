import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from sympy import *
from math import *


def derivative(func):
    x = Symbol("x")    
    return eval(func.replace("x", "Symbol('x')")).diff(x)

def antiderivative(func):
    return integrate(func).__repr__()

def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)

        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.graphic.clear()
        self.s = int(self.start.text())
        self.t = int(self.to.text())
        #self.build(self.func.text())
        print("Function:", self.func.text())
        #self.build(derivative(self.func.text()))
        print("Derivative:", derivative(self.func.text()))
        #self.build(antiderivative(self.func.text()))
        print("Antiderivative:", antiderivative(self.func.text()))
        
        
        
        
    def build(self, func):
        try:
            print(func)
            self.f = []
            for i in frange(float(self.s), float(self.t + 1), 0.1):   
                x = i
                try:
                    self.f.append(eval(func))
                except Exception:
                    self.f.append(0)
            
            self.graphic.plot([i for i in frange(float(self.s), float(self.t + 1), 0.1)],
                              self.f, pen='w')
            print(self.f, [i for i in frange(float(self.s), float(self.t + 1), 0.1)])
            print(func)
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
