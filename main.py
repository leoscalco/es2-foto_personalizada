
from source.mainWindowWidget import *
from source.ImageHandler import *
# from canon import camera
import cv2, cv, PIL
import os

# cam = camera.find()
# cam
imHandler = ImageHandler(100)

__backgroundColor__ = [200,200,200]

def onCapture(frame, currentTime):
    # TODO: Melhorar o acesso a pastas melhorar o referenciamento a elas tambem
    processedName = 'img' + str(currentTime)
    name = 'images/inputs/' + processedName + '.png'
    processedName = processedName + '.png'

    cv.SaveImage(name, frame)
    Qimg = OpenCVQImage(frame)

    bytes=Qimg.bits().asstring(Qimg.numBytes())
    img = Image.frombytes("RGB",(Qimg.width(),Qimg.height()),bytes)

    backgroundsLocation = os.getcwd() + '/images/backgrounds';

    # FIXME: Melhorar desempenho desta funcao
    imHandler.remove_background(img, __backgroundColor__, processedName)

    for i, background in enumerate(os.listdir(backgroundsLocation)):
        background = 'images/backgrounds/' + background
        background = background.lower()

        # Aplica background e salva para cada imagem de background
        # TODO: adicionar mais extensoes
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

    window = MainWindowWidget()
    window.capture.connect(onCapture)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
