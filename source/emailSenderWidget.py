import sys
import os
import time

from PyQt4 import QtCore
from PyQt4 import QtGui
from EmailSender import *

class EmailSenderWidget(QtGui.QWidget):

    def __init__(self, path):
        super(QtGui.QWidget, self).__init__()
        self.path_to_email = path
        self.initUI(path)

    def initUI(self,path):

        okButton = QtGui.QPushButton("Aceitar")
        okButton.clicked.connect(self._showDialog)
        cancelButton = QtGui.QPushButton("Cancelar")
        cancelButton.clicked.connect(self._cancel)

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

    def _cancel(self):
        self.close()
