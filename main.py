
from source.window import *
from source.ImageHandler import *
from source.FinalPhotoSelect import *
import cv2, cv,PIL

imHandler = ImageHandler(100)


def onCapture(frame, currentTime):

    #currentTime = str(datetime.datetime.now())

    processedName = 'img' + str(currentTime)
    name = 'images/inputs/' + processedName + '.png'
    processedName = processedName + '.png'

    cv.SaveImage(name, frame)
    Qimg = OpenCVQImage(frame)

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
    window.capture.connect(onCapture)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
