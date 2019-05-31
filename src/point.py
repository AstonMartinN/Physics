import sys, random, math
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer
import scipy.linalg as sla
import numpy as np


def step(Y, F, n):
    h = 0.2
    #h = 0.2
    mu = 1.0
    tau = 0.01
    d = (mu * tau) / (h * h)
    ANS = np.zeros((100, 100), dtype=np.float)
    #print(d)
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            ANS[i][j] = Y[i][j] + d*(Y[i - 1][j] + Y[i + 1][j] + Y[i][j - 1] + Y[i][j + 1] - 4 * Y[i][j]) #+ tau * F[i][j]
            if ANS[i][j] < 1.0:
                ANS[i][j] = 0
            #if ANS[i][j] > 255:
                #print(ANS[i][j])
    return ANS


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setGeometry(500, 500, 100, 100)
        self.setWindowTitle('Points')
        self.show()
        self.scrTimer = QTimer(self)
        self.scrTimer.setInterval(500)
        self.scrTimer.timeout.connect(self.update)
        self.scrTimer.start()
        self.Y1 = np.zeros((100, 100), dtype=np.float)
        self.Y2 = np.zeros((100, 100), dtype=np.float)
        self.F = np.zeros((100, 100), dtype=np.float)

    def paintEvent(self, e):
        #print(self.F)
        qp = QPainter()
        qp.begin(self)
        self.Y2 = (step(self.Y1, self.F, 100)).view()
        self.Y1 = self.Y2.view()
        self.drawPoints(qp)
        self.F = (np.zeros((100, 100), dtype=np.float)).view()
        qp.end()

    def mousePressEvent(self, event):
        #self.F[event.pos().x()][event.pos().y()] = self.F[event.pos().x()][event.pos().y()] + 5
        self.Y1[event.pos().x()][event.pos().y()] += 6000


    def drawPoints(self, qp):
        for i in range(100):
            for j in range(100):
                if self.Y1[i][j] < 255:
                    qp.setPen(QColor(255, 255 - self.Y1[i][j] , 255 - self.Y1[i][j] ))
                else:
                    qp.setPen(QColor(255 , 0 , 0 ) )
                qp.drawPoint(i, j)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.scrTimer.stop()
            self.close()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
