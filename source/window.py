import sys
import os

from PyQt4 import QtCore
from PyQt4 import QtGui


from source.camera import *

class WindowWidget(QtGui.QMainWindow):

    camera = QtCore.pyqtSignal()
    capture = QtCore.pyqtSignal(cv.iplimage, str)
    background = QtCore.pyqtSignal();
    backgroundPath = ''

    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        self.setMinimumSize(800,640)
        self.setWindowTitle('Awesome Window')

        self.init_ui()

    def init_ui(self):

        cameraDevice = CameraDevice(mirrored=True,parent=self)
        self.cameraWidget = CameraWidget(cameraDevice,self)
        self.cameraWidget.show()

        #############
        menuContainer = QtGui.QWidget(self)
        menuContainer.setMinimumSize(400,40)
        menuLayout = QtGui.QHBoxLayout()

        cameraButton = QtGui.QPushButton("CAMERA")
        cameraButton.setMinimumSize(100,40)
        cameraButton.clicked.connect(self._clickedCamera)
        menuLayout.addWidget(cameraButton)

        captureButton = QtGui.QPushButton("CAPTURE")
        captureButton.setMinimumSize(100,40)
        captureButton.clicked.connect(self._clickedCapture)
        menuLayout.addWidget(captureButton)

        backgroundSelectButton = QtGui.QPushButton("BACKGROUND")
        backgroundSelectButton.setMinimumSize(100,40)
        backgroundSelectButton.clicked.connect(self._clickedBackgroundSelec)
        menuLayout.addWidget(backgroundSelectButton)

        menuContainer.setLayout(menuLayout)
        menuContainer.show()

        #############

        self.show()


    def _clickedCapture(self):
        self.capture.emit(self.cameraWidget._frame, self.backgroundPath)

    def _clickedCamera(self):
        self.camera.emit()

    def _clickedBackgroundSelec(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                os.getcwd() + '/images/backgrounds')
        fname = fname[str(fname).find("images/backgrounds/"):]
        self.backgroundPath = str(fname)
        print(self.backgroundPath)

