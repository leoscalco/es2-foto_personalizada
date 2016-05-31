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
        self.setMinimumSize(320,240)
        self.setWindowTitle('Awesome Window')
        self.init_ui()

    def init_ui(self):

        cameraDevice = CameraDevice(mirrored=True,parent=self)
        self.cameraWidget = CameraWidget(cameraDevice,self)
        self.cameraWidget.show()

        # Ajusta a janela para o tamanho da imagem da camera
        self.setGeometry(0, 0,self.cameraWidget.width(), self.cameraWidget.height())

        menuContainer = QtGui.QWidget(self)
        menuContainer.setMinimumSize(320,40)
        menuLayout = QtGui.QHBoxLayout()

        #############

        captureButton = QtGui.QPushButton("Capture")
        captureButton.setMinimumSize(50,40)
        captureButton.clicked.connect(self._clickedCapture)

        spacer = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        menuLayout.addWidget(captureButton)
        # menuLayout.addWidget(backgroundSelectButton)
        menuLayout.addSpacerItem(spacer)
        menuContainer.setLayout(menuLayout)
        menuContainer.show()

        #############

        self.show()

    def _clickedCapture(self):
        self.currentTime = str(time.ctime())
        self.capture.emit(self.cameraWidget._frame, self.currentTime)
        self.finalPhotoWindow = FinalPhotoWidget(self.currentTime)
