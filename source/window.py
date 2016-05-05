import sys

from PyQt4 import QtCore
from PyQt4 import QtGui

from source.camera import *

class WindowWidget(QtGui.QMainWindow):

    camera = QtCore.pyqtSignal()
    capture = QtCore.pyqtSignal(cv.iplimage)

    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        self.setFixedSize(800,640)
        self.setWindowTitle('Awesome Window')

        self.init_ui()

    def init_ui(self):

        cameraDevice = CameraDevice(mirrored=True,parent=self)
        self.cameraWidget = CameraWidget(cameraDevice,self)
        self.cameraWidget.show()

        #############
        menuContainer = QtGui.QWidget(self)
        menuContainer.setMinimumSize(160,20)
        menuLayout = QtGui.QHBoxLayout()

        cameraButton = QtGui.QPushButton("CAMERA")
        cameraButton.clicked.connect(self._clickedCamera)
        menuLayout.addWidget(cameraButton)

        captureButton = QtGui.QPushButton("CAPTURE")
        captureButton.clicked.connect(self._clickedCapture)
        menuLayout.addWidget(captureButton)

        menuContainer.setLayout(menuLayout)
        menuContainer.show()
        #############

        self.show()

    def _clickedCapture(self):
        self.capture.emit(self.cameraWidget._frame)

    def _clickedCamera(self):
        self.camera.emit()
