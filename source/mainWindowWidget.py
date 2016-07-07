import sys
import os
import time

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import *

from cameraWidget import *
from finalPhotoWidget import *

class MainWindowWidget(QtGui.QMainWindow):

    capture = QtCore.pyqtSignal(cv.iplimage, str)
    background = QtCore.pyqtSignal();
    backgroundPath = ''

    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)

        # FIXME: Melhorar questao de tamanho de janela desta classe
        self.setMinimumSize(320,240)
        self.setWindowTitle('Awesome Window')
        self.init_ui()

    def init_ui(self):

        cameraDevice = CameraDevice(mirrored=True,parent=self)
        self.cameraWidget = CameraWidget(cameraDevice,self)
        self.cameraWidget.show()

        # Ajusta a posicao da camera para o centro da janela
        self.cameraWidget.move(QtGui.QApplication.desktop().screen().rect().center() - self.cameraWidget.rect().center())

        # Ajusta a janela para o tamanho da tela do computador
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, resolution.width(), resolution.height())

        # TODO: Melhorar o layout dos botoes
        menuContainer = QtGui.QWidget(self)
        menuContainer.setMinimumSize(320,40)
        menuLayout = QtGui.QHBoxLayout()

        #############
        captureButton = QtGui.QPushButton("Capturar")
        captureButton.setMinimumSize(50,40)
        captureButton.clicked.connect(self._clickedCapture)

        spacer = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        menuLayout.addWidget(captureButton)
        menuLayout.addSpacerItem(spacer)
        menuContainer.setLayout(menuLayout)
        menuContainer.show()
        #############
        self.show()

    def _clickedCapture(self):
        # MainWindow nao deveria se importar com currentTime
        # Na 'Capture.emit' os backgrounds sao removidos.
        # Estas funcoes poderiam ser repassadas para uma classe terceira.
        self.currentTime = str(time.ctime())
        self.capture.emit(self.cameraWidget._frame, self.currentTime)
        self.finalPhotoWindow = FinalPhotoWidget(self.currentTime)
