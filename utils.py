from PySide2.QtWidgets import QMainWindow
from shiboken2 import shiboken2
from maya import OpenMayaUI


def getMayaMainWindow():
    pointer = OpenMayaUI.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(pointer), QMainWindow)