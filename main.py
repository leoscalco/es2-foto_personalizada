
from source.window import *

def onCamera():
    # Entrando em modo live da camera
    print('Camera!')

def onCapture(frame):
    # Entrando em modo de captura
    #   grab the photo!!
    print('Capture!')
    w, h = cv.GetSize(frame)
    # FIXME: Crop por width e height para caber na janela


def main():

    app = QtGui.QApplication(sys.argv)

    window = WindowWidget()
    window.camera.connect(onCamera)
    window.capture.connect(onCapture)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
