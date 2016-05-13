
from source.window import *
from source.ImageHandler import *
import cv2, cv,PIL
import datetime

imHandler = ImageHandler(100)

def onCamera():
    # Entrando em modo live da camera
    print('Camera!')

def onCapture(frame, backgroundPath):

    processedName = 'img' + str(datetime.datetime.now())
    name = 'images/inputs/' + processedName + '.jpg'
    processedName = processedName + '.png'

    cv.SaveImage(name,frame)
    Qimg = OpenCVQImage(frame)

    print('Capture!')


    bytes=Qimg.bits().asstring(Qimg.numBytes())
    img = Image.frombytes("RGB",(Qimg.width(),Qimg.height()),bytes)

    imHandler.remove_background(img,[200,200,200], processedName)
    background = PIL.Image.open(str(backgroundPath))
    imHandler.put_background(background, processedName)





def main():

    app = QtGui.QApplication(sys.argv)
    window = WindowWidget()
    window.camera.connect(onCamera)
    window.capture.connect(onCapture)

    

    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
