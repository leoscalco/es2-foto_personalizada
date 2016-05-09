
from source.window import *
from source.ImageHandler import *
import cv2, cv,PIL
import datetime

imHandler = ImageHandler(100)

def onCamera():
    # Entrando em modo live da camera
    print('Camera!')

def onCapture(frame):
    name = 'images/inputs/img'+str(datetime.datetime.now())+'.jpg'

    cv.SaveImage(name,frame)
    Qimg = OpenCVQImage(frame)

    print('Capture!')

    bytes=Qimg.bits().asstring(Qimg.numBytes())
    img = Image.frombytes("RGB",(Qimg.width(),Qimg.height()),bytes)

    imHandler.remove_background(img,[200,200,200])
    background = PIL.Image.open("images/backgrounds/ECOMUSEU.jpg")
    imHandler.put_background(background)


def main():

    app = QtGui.QApplication(sys.argv)

    window = WindowWidget()
    window.camera.connect(onCamera)
    window.capture.connect(onCapture)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
