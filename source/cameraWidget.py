# Code from Rafael Barreto
# at: https://rafaelbarreto.wordpress.com/2011/08/27/a-pyqt-widget-for-opencv-camera-preview/

import cv

from PyQt4 import QtCore
from PyQt4 import QtGui

class OpenCVQImage(QtGui.QImage):

    def __init__(self, opencvBgrImg):
        depth, nChannels = opencvBgrImg.depth, opencvBgrImg.nChannels
        if depth != cv.IPL_DEPTH_8U or nChannels != 3:
            raise ValueError("the input image must be 8-bit, 3-channel")
        w, h = cv.GetSize(opencvBgrImg)
        opencvRgbImg = cv.CreateImage((w, h), depth, nChannels)
        # it's assumed the image is in BGR format
        cv.CvtColor(opencvBgrImg, opencvRgbImg, cv.CV_BGR2RGB)
        self._imgData = opencvRgbImg.tostring()
        super(OpenCVQImage, self).__init__(self._imgData, w, h, \
            QtGui.QImage.Format_RGB888)

class CameraDevice(QtCore.QObject):

    _DEFAULT_FPS = 30

    newFrame = QtCore.pyqtSignal(cv.iplimage)

    def __init__(self, cameraId=0, mirrored=False, parent=None):
        super(CameraDevice, self).__init__(parent)

        self.mirrored = mirrored

        self._cameraDevice = cv.CaptureFromCAM(cameraId)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(1000/self.fps)

        self.paused = False

    @QtCore.pyqtSlot()
    def _queryFrame(self):
        frame = cv.QueryFrame(self._cameraDevice)
        if self.mirrored:
            mirroredFrame = cv.CreateImage(cv.GetSize(frame), frame.depth, \
                frame.nChannels)
            cv.Flip(frame, mirroredFrame, 1)
            frame = mirroredFrame
        self.newFrame.emit(frame)

    @property
    def paused(self):
        return not self._timer.isActive()

    @paused.setter
    def paused(self, p):
        if p:
            self._timer.stop()
        else:
            self._timer.start()

    @property
    def frameSize(self):
        w = cv.GetCaptureProperty(self._cameraDevice, \
            cv.CV_CAP_PROP_FRAME_WIDTH)
        h = cv.GetCaptureProperty(self._cameraDevice, \
            cv.CV_CAP_PROP_FRAME_HEIGHT)
        return int(w), int(h)

    @property
    def fps(self):
        fps = int(cv.GetCaptureProperty(self._cameraDevice, cv.CV_CAP_PROP_FPS))
        if not fps > 0:
            fps = self._DEFAULT_FPS
        return fps

class CameraWidget(QtGui.QWidget):

    _frame = None
    newFrame = QtCore.pyqtSignal(cv.iplimage)

    def __init__(self, cameraDevice, parent=None):
        super(CameraWidget, self).__init__(parent)

        self._frame = None

        self._cameraDevice = cameraDevice
        self._cameraDevice.newFrame.connect(self._onNewFrame)

        w, h = self._cameraDevice.frameSize
        self.setMinimumSize(w, h)
        self.setMaximumSize(w, h)

    def querySingleFrame(self):
        return self._cameraDevice.querySingleFrame()

    @QtCore.pyqtSlot(cv.iplimage)
    def _onNewFrame(self, frame):
        self._frame = cv.CloneImage(frame)
        self.newFrame.emit(self._frame)
        self.update()

    def changeEvent(self, e):
        if e.type() == QtCore.QEvent.EnabledChange:
            if self.isEnabled():
                self._cameraDevice.newFrame.connect(self._onNewFrame)
            else:
                self._cameraDevice.newFrame.disconnect(self._onNewFrame)

    def paintEvent(self, e):
        if self._frame is None:
            return
        painter = QtGui.QPainter(self)
        painter.drawImage(QtCore.QPoint(0, 0), OpenCVQImage(self._frame))
