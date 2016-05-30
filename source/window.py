import sys
import os
import time

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import *
from EmailSender import *
from os import walk

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
        #self.currentTime = str(datetime.datetime.now())
        self.currentTime = str(time.ctime())
        self.capture.emit(self.cameraWidget._frame, self.currentTime)
        self.test = FinalPhotoSelect(self.currentTime)
        
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


class FinalPhotoSelect(QtGui.QWidget):

    def __init__(self, currentTime):
        super(FinalPhotoSelect, self).__init__()
        self.currentTime = currentTime
        self.initUI()

    def initUI(self):
        self.resize(640,480)
        self.layout = QtGui.QVBoxLayout(self)

        self.scene = QtGui.QGraphicsScene(self)
        self.view = QtGui.QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.image = QtGui.QGraphicsPixmapItem()
        self.scene.addItem(self.image)
        self.view.centerOn(self.image)
        self._images = []
        
        for file in os.listdir(os.getcwd() + '/images/outputs'):
            if self.currentTime in file:
                if 'transparent' not in file:
                    print file
                    self._images.append(QtGui.QPixmap('images/outputs/' + file))

        self.slider = QtGui.QSlider(self)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        # max is the last index of the image list
        self.slider.setMaximum(len(self._images)-1)
        self.layout.addWidget(self.slider)

        # set it to the first image, if you want.
        self.sliderMoved(0)

        self.slider.sliderMoved.connect(self.sliderMoved)

        self.show()

    def sliderMoved(self, val):
        print "Slider moved to:", val
        try:
            self.image.setPixmap(self._images[val])
        except IndexError:
            print "Error: No image at index", val

# if __name__ == "__main__":
#     app = QtGui.QApplication([])
#     w = FinalPhotoSelect()
#     w.show()
#     w.raise_()
#     app.exec_()
