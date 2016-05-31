
from source.window import *
from source.ImageHandler import *
import cv2, cv,PIL
import os

imHandler = ImageHandler(100)


def onCapture(frame, currentTime):

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
        background = background.lower()
        #background = PIL.Image.open(str(backgroundPath))
        #imHandler.put_background(background, processedName)

        # Aplica background e salva para cada imagem de background
        if background.endswith(".jpg") or background.endswith(".png"):
            teste = PIL.Image.open(str(background))
            imHandler.put_background(teste, `i` + processedName)

def criaDiretorioSeNaoExistir():
    dirs = ['images',
        'images/outputs',
        'images/inputs',
        'images/backgrounds']
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

def main():

    criaDiretorioSeNaoExistir()

    app = QtGui.QApplication(sys.argv)

    window = WindowWidget()
    window.capture.connect(onCapture)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
