
from source.window import *
from source.ImageHandler import *
import cv2, cv,PIL
import datetime

imHandler = ImageHandler(100)

def onCamera():
    # Entrando em modo live da camera
    print('Camera!')

def onCapture(frame, backgroundPath):

    currentTime = str(datetime.datetime.now())

    processedName = 'img' + currentTime
    name = 'images/inputs/' + processedName + '.jpg'
    processedName = processedName + '.png'

    cv.SaveImage(name, frame)
    Qimg = OpenCVQImage(frame)

    print('Capture!')


    bytes=Qimg.bits().asstring(Qimg.numBytes())
    img = Image.frombytes("RGB",(Qimg.width(),Qimg.height()),bytes)

    backgroundsLocation = os.getcwd() + '/images/backgrounds';

    imHandler.remove_background(img,[200,200,200], processedName)

    for i, background in enumerate(os.listdir(backgroundsLocation)):    
        background = 'images/backgrounds/' + background
        #background = PIL.Image.open(str(backgroundPath))
        #imHandler.put_background(background, processedName)
        if background.endswith(".jpg"):
            teste = PIL.Image.open(str(background))
            imHandler.put_background(teste, `i` + processedName)





def main():

    app = QtGui.QApplication(sys.argv)
    window = WindowWidget()
    window.camera.connect(onCamera)
    window.capture.connect(onCapture)

    

    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
