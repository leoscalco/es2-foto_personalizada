from PyQt4 import QtCore, QtGui
import os
from os import walk

class FinalPhotoSelect(QtGui.QWidget):

    def __init__(self, parent=None):
        super(FinalPhotoSelect, self).__init__(parent)
        self.resize(640,480)
        self.layout = QtGui.QVBoxLayout(self)

        self.scene = QtGui.QGraphicsScene(self)
        self.view = QtGui.QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.image = QtGui.QGraphicsPixmapItem()
        self.scene.addItem(self.image)
        self.view.centerOn(self.image)
        self._images = []
        
        for file in os.listdir(os.getcwd() + '/images/backgrounds'):
            if file.endswith(".jpg"):
                self._images.append(QtGui.QPixmap(file))
        
        # self._images = [
        #     QtGui.QPixmap('Smiley1.jpg'),
        #     QtGui.QPixmap('Smiley2.jpg'),
        #     QtGui.QPixmap('Smiley3.jpg')
        # ]

        self.slider = QtGui.QSlider(self)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        # max is the last index of the image list
        self.slider.setMaximum(len(self._images)-1)
        self.layout.addWidget(self.slider)

        # set it to the first image, if you want.
        self.sliderMoved(0)

        self.slider.sliderMoved.connect(self.sliderMoved)

    def sliderMoved(self, val):
        print "Slider moved to:", val
        try:
            self.image.setPixmap(self._images[val])
        except IndexError:
            print "Error: No image at index", val

if __name__ == "__main__":
    app = QtGui.QApplication([])
    w = FinalPhotoSelect()
    w.show()
    w.raise_()
    app.exec_()