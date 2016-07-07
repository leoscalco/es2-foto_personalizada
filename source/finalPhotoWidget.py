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
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, resolution.width(), resolution.height())
        self.layout = QtGui.QVBoxLayout(self)

        self.scene = QtGui.QGraphicsScene(self)
        self.view = QtGui.QGraphicsView(self.scene)

        self.image = QtGui.QGraphicsPixmapItem()
        self.scene.addItem(self.image)
        self.view.centerOn(self.image)
        self._images = []
        self._imagesPaths = []

        self.imageListWidget = QtGui.QListWidget(self)
        self.imageListWidget.setMinimumHeight(110)
        self.imageListWidget.setViewMode(1)
        self.imageListWidget.setIconSize(QtCore.QSize(135,120))
        self.imageListWidget.setResizeMode(0)
        self.imageListWidget.setMaximumHeight(110)

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
        self.layout.addWidget(self.imageListWidget)

        self.show()

        for file in os.listdir(os.getcwd() + '/images/outputs'):
            if self.currentTime in file:
                if 'transparent' not in file:
                    print file
                    self._images.append(QtGui.QPixmap('images/outputs/' + file).scaled(self.view.width() - 5, self.view.height() - 5, QtCore.Qt.KeepAspectRatio))
                    self.imageListWidget.addItem(QtGui.QListWidgetItem(QtGui.QIcon("images/outputs/" + file), ""))
                    self._imagesPaths.append(os.getcwd() + '/images/outputs/' + file)


        self.imageListWidget.itemClicked.connect(self.thumbClicked)
        self.imageListWidget.setCurrentRow(0)
        self.thumbClicked(0)


        print self.view.width()
        print self.view.height()

    def thumbClicked(self, thumbnail):
        try:
            self.image.setPixmap(self._images[self.imageListWidget.currentRow()])
            self.currentImageIndex = self.imageListWidget.currentRow()
        except IndexError:
            print "Error: No image at index", self.imageListWidget.currentRow()

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