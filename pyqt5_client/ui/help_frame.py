# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/help_frame.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(551, 447)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/resources/icon/帮助.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Frame.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(150, 90, 72, 15))
        self.label.setObjectName("label")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "帮助"))
        self.label.setText(_translate("Frame", "帮助"))
import apprcc_rc
