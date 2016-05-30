import sys
import os

from PyQt4 import QtCore
from PyQt4 import *
from EmailSender import *


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

        # backgroundSelectButton = QtGui.QPushButton("BACKGROUND")
        # backgroundSelectButton.setMinimumSize(100,40)
        # backgroundSelectButton.clicked.connect(self._clickedBackgroundSelec)
        # menuLayout.addWidget(backgroundSelectButton)

        menuContainer.setLayout(menuLayout)
        menuContainer.show()

        #############

        self.show()



    def _clickedCapture(self):
        self.capture.emit(self.cameraWidget._frame, self.backgroundPath)
        
    def _clickedCamera(self):
        self.camera.emit()

    # def _clickedBackgroundSelec(self):
    #     fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
    #             os.getcwd() + '/images/backgrounds')
    #     fname = fname[str(fname).find("images/backgrounds/"):]
    #     self.backgroundPath = str(fname)
    #     print(self.backgroundPath)


class imgWindowWidget(QtGui.QWidget):
    
    def __init__(self, path):
        super(QtGui.QWidget, self).__init__()
        self.path_to_email = path
        self.initUI(path)
        
    def initUI(self,path):
        
        okButton = QtGui.QPushButton("Aceitar")
        okButton.clicked.connect(self._showDialog)
        cancelButton = QtGui.QPushButton("Cancelar")

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)   
        ibox = QtGui.QHBoxLayout(self)
        imageMap = QtGui.QPixmap(path)
        imageMap = imageMap.scaled(640, 480, QtCore.Qt.KeepAspectRatio) 
        label = QtGui.QLabel(self)
        label.setPixmap(imageMap)
        ibox.addWidget(label)
        label.setGeometry(0,0,640,480)
        
        
        self.setGeometry(0, 0, 800, 640)
        self.setWindowTitle('Imagem Resultante')  

        self.show()
        
       

    def _showDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Email Input', 
            'Insira seu email')
        
        if ok:

            emailsender = EmailSender('smtp.gmail.com', 587)
            print(str(text))
            try:
                emailsender.login("63u.r2Y.R9n.9q5@gmail.com", "QpG-6ey-EJu-DwP")
                print self.path_to_email
                emailsender.send_with_attachment(str(text), "Teste de envio com software", "body", self.path_to_email)
                emailsender.quit()
            except Exception, e:
                print "Error!"
                print str(e)

