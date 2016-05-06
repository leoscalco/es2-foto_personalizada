
from source.window import *
import cv2, cv
import datetime
def onCamera():
    # Entrando em modo live da camera
    print('Camera!')

def onCapture(frame):
    name = 'capturedImg/img'+str(datetime.datetime.now())+'.jpg'

    cv.SaveImage(name,frame)
    
    print('Capture!')
    w, h = cv.GetSize(frame)
    


def main():

    app = QtGui.QApplication(sys.argv)

    window = WindowWidget()
    window.camera.connect(onCamera)
    window.capture.connect(onCapture)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
opepenc