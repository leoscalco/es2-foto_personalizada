import sys
import os
import time

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import *

from emailSenderWidget import *

class FinalPhotoWidget(QtGui.QWidget):

    def __init__(self, currentTime):
        super(QtGui.QWidget, self).__init__()
        self.currentTime = currentTime
        self.initUI()

    def initUI(self):
        self.resize(640,480)
        self.layout = QtGui.QVBoxLayout(self)

        self.scene = QtGui.QGraphicsScene(self)
        self.view = QtGui.QGraphicsView(self.scene)

        self.image = QtGui.QGraphicsPixmapItem()
        self.scene.addItem(self.image)
        self.view.centerOn(self.image)
        self._images = []
        self._imagesPaths = []

        for file in os.listdir(os.getcwd() + '/images/outputs'):
            if self.currentTime in file:
                if 'transparent' not in file:
                    print file
                    self._images.append(QtGui.QPixmap('images/outputs/' + file))
                    self._imagesPaths.append(os.getcwd() + '/images/outputs/' + file)

        self.slider = QtGui.QSlider(self)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        
        self.slider.setMaximum(len(self._images)-1)

        menuContainer = QtGui.QWidget(self)
        menuContainer.setMinimumSize(320,40)
        menuLayout = QtGui.QHBoxLayout()

        selectButton = QtGui.QPushButton("Escolher")
        selectButton.setMinimumSize(50,40)
        selectButton.clicked.connect(self._clickedSelect)

        cancelarButton = QtGui.QPushButton("Cancelar")
        cancelarButton.setMinimumSize(50,40)
        cancelarButton.clicked.connect(self._cickedCancel)

        spacer = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        menuLayout.addWidget(selectButton)
        menuLayout.addWidget(cancelarButton)
        menuLayout.addSpacerItem(spacer)
        menuContainer.setLayout(menuLayout)
        menuContainer.show()

        self.layout.addWidget(menuContainer)
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.slider)

        # set it to the first image, if you want.
        self.sliderMoved(0)
        self.slider.sliderMoved.connect(self.sliderMoved)
        self.show()

    def sliderMoved(self, val):
        try:
            self.image.setPixmap(self._images[val])
            self.currentImageIndex = val
        except IndexError:
            print "Error: No image at index", val

    def _clickedSelect(self):
        print self.currentImageIndex
        self.photoPath =  self._images[self.currentImageIndex]
        self._showEmailDialog()

    def _cickedCancel(self):
        self.close()

    def _showEmailDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Email Input',
            'Insira seu email')

        if ok:
            emailsender = EmailSender('smtp.gmail.com', 587)
            print(str(text))
            try:
                emailsender.login("63u.r2Y.R9n.9q5@gmail.com", "QpG-6ey-EJu-DwP")
                emailsender.send_with_attachment(str(text), "Teste de envio com software", "body", self._imagesPaths[self.currentImageIndex])
                emailsender.quit()
            except Exception, e:
                print "Error!"
                print str(e)