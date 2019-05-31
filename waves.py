import sys, random, math
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer
import scipy.linalg as sla
import numpy as np


def step(Y0, Y1, n):
    h = 0.2
    c = 1.0
    tau = 0.1 #0.01
    d = ((tau * c) / h) ** 2
    #print(d)
    ANS = np.zeros((100, 100), dtype=np.float)
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            ANS[i][j] = 2 * Y1[i][j] - Y0[i][j] + d*(  Y1[i - 1][j] + Y1[i + 1][j] + Y1[i][j - 1] + Y1[i][j + 1] - 4 * Y1[i][j]   )
            if ANS[i][j] < 1.0 :
                ANS[i][j] = 0
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
        self.scrTimer.setInterval(200)
        self.scrTimer.timeout.connect(self.update)
        self.scrTimer.start()
        self.Y1 = np.zeros((100, 100), dtype=np.float)
        self.Y2 = np.zeros((100, 100), dtype=np.float)
        self.Y3 = np.zeros((100, 100), dtype=np.float)

    def paintEvent(self, e):
        #print(self.F)
        qp = QPainter()
        qp.begin(self)
        self.Y3 = step(self.Y1, self.Y2, 100)
        self.Y1 = self.Y2.view()
        self.Y2 = self.Y3.view()
        self.drawPoints(qp)
        qp.end()

    def mousePressEvent(self, event):
        self.Y2[event.pos().x()][event.pos().y()] += 2000


    def drawPoints(self, qp):
        for i in range(100):
            for j in range(100):
                if self.Y1[i][j] < 255:
                    qp.setPen(QColor(255 - self.Y1[i][j], 255 - self.Y1[i][j] , 255 ))
                else:
                    qp.setPen(QColor(0 , 0 , 255 ) )
                qp.drawPoint(i, j)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.scrTimer.stop()
            self.close()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
